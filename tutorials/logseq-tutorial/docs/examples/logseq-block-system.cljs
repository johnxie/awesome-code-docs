;; Logseq Block-Based Architecture Implementation
;; 
;; This file demonstrates core patterns in Logseq's block-centric knowledge management:
;; - Block data modeling and storage
;; - Bi-directional linking system
;; - Graph traversal and querying
;; - Real-time collaborative editing
;; - Plugin architecture and extensibility
;; 
;; Key concepts covered:
;; - File-based storage with Git synchronization
;; - ClojureScript + Electron desktop architecture
;; - Advanced graph visualization and navigation
;; - Local-first data management patterns

(ns logseq.examples.block-system
  (:require [clojure.string :as str]
            [clojure.set :as set]
            [cljs.core.async :as async :refer [<! >! chan go go-loop]]
            [re-frame.core :as rf]
            [datascript.core :as d]
            [logseq.db.schema :as db-schema]
            [logseq.util :as util]
            [goog.object :as gobj]))

;; =============================================================================
;; Core Data Models & Schema
;; =============================================================================

(def logseq-schema
  "Logseq's DataScript schema for block-based knowledge management"
  {:block/uuid          {:db/unique :db.unique/identity}
   :block/left          {:db/valueType :db.type/ref}
   :block/parent        {:db/valueType :db.type/ref}
   :block/page          {:db/valueType :db.type/ref}
   :block/refs          {:db/valueType :db.type/ref
                         :db/cardinality :db.cardinality/many}
   :block/path-refs     {:db/valueType :db.type/ref
                         :db/cardinality :db.cardinality/many}
   :block/tags          {:db/valueType :db.type/ref
                         :db/cardinality :db.cardinality/many}
   :block/content       {}
   :block/marker        {}
   :block/priority      {}
   :block/properties    {}
   :block/pre-block?    {}
   :block/created-at    {}
   :block/updated-at    {}
   :block/file          {:db/valueType :db.type/ref}
   
   ;; Page schema
   :page/name           {:db/unique :db.unique/identity}
   :page/original-name  {:db/unique :db.unique/identity}
   :page/alias          {:db/valueType :db.type/ref
                         :db/cardinality :db.cardinality/many}
   :page/tags           {:db/valueType :db.type/ref
                         :db/cardinality :db.cardinality/many}
   :page/properties     {}
   :page/created-at     {}
   :page/updated-at     {}
   :page/file           {:db/valueType :db.type/ref}
   
   ;; File schema
   :file/path           {:db/unique :db.unique/identity}
   :file/content        {}
   :file/created-at     {}
   :file/last-modified-at {}
   :file/size           {}})

;; Block data structure
(defrecord Block [uuid content properties parent left page refs tags 
                  marker priority pre-block? created-at updated-at file])

(defrecord Page [name original-name alias tags properties 
                 created-at updated-at file])

(defrecord File [path content created-at last-modified-at size])

;; =============================================================================
;; Block Operations & Management
;; =============================================================================

(defn generate-block-uuid
  "Generate a unique UUID for a new block"
  []
  (str (random-uuid)))

(defn create-block
  "Create a new block with optional properties"
  ([content]
   (create-block content {}))
  ([content options]
   (map->Block
    (merge
     {:uuid (generate-block-uuid)
      :content content
      :properties {}
      :refs []
      :tags []
      :created-at (js/Date.)
      :updated-at (js/Date.)
      :pre-block? false}
     options))))

(defn block-with-refs
  "Extract page references from block content and create refs"
  [db block]
  (let [content (:content block)
        ;; Extract [[Page Name]] references
        page-refs (re-seq #"\[\[([^\]]+)\]\]" content)
        ;; Extract #tag references  
        tag-refs (re-seq #"#([^\s\[\](){}]+)" content)
        ;; Get page entities for refs
        ref-pages (mapv (fn [[_ page-name]]
                         (or (d/entity db [:page/name page-name])
                             ;; Create page if it doesn't exist
                             (create-page-if-not-exists db page-name)))
                       page-refs)
        tag-pages (mapv (fn [[_ tag-name]]
                         (or (d/entity db [:page/name tag-name])
                             (create-page-if-not-exists db tag-name)))
                       tag-refs)]
    (assoc block 
           :refs ref-pages
           :tags tag-pages)))

(defn insert-block
  "Insert a block into the database with proper relationships"
  [db block]
  (let [block-with-refs (block-with-refs db block)
        tx-data [{:block/uuid (:uuid block-with-refs)
                  :block/content (:content block-with-refs)
                  :block/properties (:properties block-with-refs)
                  :block/parent (:parent block-with-refs)
                  :block/left (:left block-with-refs)
                  :block/page (:page block-with-refs)
                  :block/refs (mapv :db/id (:refs block-with-refs))
                  :block/tags (mapv :db/id (:tags block-with-refs))
                  :block/marker (:marker block-with-refs)
                  :block/priority (:priority block-with-refs)
                  :block/pre-block? (:pre-block? block-with-refs)
                  :block/created-at (:created-at block-with-refs)
                  :block/updated-at (:updated-at block-with-refs)
                  :block/file (:file block-with-refs)}]]
    (d/transact! db tx-data)))

(defn update-block
  "Update an existing block's content and properties"
  [db block-uuid updates]
  (let [block (d/entity db [:block/uuid block-uuid])
        updated-block (merge block updates {:updated-at (js/Date.)})
        block-with-new-refs (block-with-refs db updated-block)]
    (d/transact! db [{:db/id (:db/id block)
                      :block/content (:content block-with-new-refs)
                      :block/properties (:properties block-with-new-refs)
                      :block/refs (mapv :db/id (:refs block-with-new-refs))
                      :block/tags (mapv :db/id (:tags block-with-new-refs))
                      :block/updated-at (:updated-at block-with-new-refs)}])))

(defn delete-block
  "Delete a block and update sibling relationships"
  [db block-uuid]
  (let [block (d/entity db [:block/uuid block-uuid])
        left-sibling (:block/left block)
        right-sibling (d/q '[:find ?e .
                            :in $ ?left
                            :where [?e :block/left ?left]]
                          db (:db/id block))
        tx-data (cond-> [[:db/retractEntity (:db/id block)]]
                  ;; Update right sibling to point to left sibling
                  (and left-sibling right-sibling)
                  (conj {:db/id right-sibling
                         :block/left (:db/id left-sibling)}))]
    (d/transact! db tx-data)))

;; =============================================================================
;; Block Hierarchy & Navigation
;; =============================================================================

(defn get-block-children
  "Get all direct children of a block"
  [db block-uuid]
  (let [block (d/entity db [:block/uuid block-uuid])]
    (d/q '[:find [(pull ?child [*]) ...]
           :in $ ?parent
           :where [?child :block/parent ?parent]]
         db (:db/id block))))

(defn get-block-tree
  "Get complete block tree starting from a root block"
  ([db block-uuid]
   (get-block-tree db block-uuid 0 10)) ; default max depth of 10
  ([db block-uuid current-depth max-depth]
   (when (<= current-depth max-depth)
     (let [block (d/entity db [:block/uuid block-uuid])
           children (get-block-children db block-uuid)]
       (assoc block
              :children (mapv #(get-block-tree db (:block/uuid %) 
                                             (inc current-depth) max-depth)
                             children)
              :depth current-depth)))))

(defn get-block-siblings
  "Get all sibling blocks (same parent) of a given block"
  [db block-uuid]
  (let [block (d/entity db [:block/uuid block-uuid])
        parent (:block/parent block)]
    (when parent
      (d/q '[:find [(pull ?sibling [*]) ...]
             :in $ ?parent ?current
             :where 
             [?sibling :block/parent ?parent]
             [(not= ?sibling ?current)]]
           db (:db/id parent) (:db/id block)))))

(defn move-block
  "Move a block to a new parent and position"
  [db block-uuid new-parent-uuid new-left-uuid]
  (let [block (d/entity db [:block/uuid block-uuid])
        new-parent (when new-parent-uuid
                    (d/entity db [:block/uuid new-parent-uuid]))
        new-left (when new-left-uuid
                  (d/entity db [:block/uuid new-left-uuid]))
        ;; Find the block that was previously to the right of new-left
        old-right (when new-left
                   (d/q '[:find ?e .
                          :in $ ?left
                          :where [?e :block/left ?left]]
                        db (:db/id new-left)))
        tx-data (cond-> [{:db/id (:db/id block)
                          :block/parent (:db/id new-parent)
                          :block/left (when new-left (:db/id new-left))}]
                  ;; Update the old right sibling to point to this block
                  old-right
                  (conj {:db/id old-right
                         :block/left (:db/id block)}))]
    (d/transact! db tx-data)))

;; =============================================================================
;; Page Management & References
;; =============================================================================

(defn create-page-if-not-exists
  "Create a page if it doesn't already exist"
  [db page-name]
  (if-let [existing-page (d/entity db [:page/name page-name])]
    existing-page
    (let [page-data {:page/name page-name
                     :page/original-name page-name
                     :page/created-at (js/Date.)
                     :page/updated-at (js/Date.)
                     :page/properties {}}]
      (d/transact! db [page-data])
      (d/entity db [:page/name page-name]))))

(defn get-page-references
  "Get all blocks that reference a specific page"
  [db page-name]
  (d/q '[:find [(pull ?block [*]) ...]
         :in $ ?page-name
         :where
         [?page :page/name ?page-name]
         [?block :block/refs ?page]]
       db page-name))

(defn get-page-backlinks
  "Get pages that link to the specified page"
  [db page-name]
  (let [referencing-blocks (get-page-references db page-name)]
    (->> referencing-blocks
         (map :block/page)
         (map #(d/entity db (:db/id %)))
         (remove #(= (:page/name %) page-name))
         distinct)))

(defn get-page-graph
  "Get the complete graph of page connections"
  [db]
  (let [pages (d/q '[:find [(pull ?page [:page/name]) ...]
                     :where [?page :page/name]]
                   db)
        connections (d/q '[:find ?source-page ?target-page
                          :where
                          [?block :block/page ?source-page]
                          [?block :block/refs ?target-page]]
                        db)]
    {:nodes pages
     :edges (mapv (fn [[source target]]
                   {:source (:page/name (d/entity db source))
                    :target (:page/name (d/entity db target))})
                 connections)}))

;; =============================================================================
;; Advanced Querying & Search
;; =============================================================================

(defn search-blocks
  "Full-text search across block content"
  [db search-term]
  (let [search-pattern (str "(?i).*" search-term ".*")]
    (d/q `[:find [(pull ?block [*]) ...]
           :where
           [?block :block/content ?content]
           [(re-find ~(re-pattern search-pattern) ?content)]]
         db)))

(defn find-blocks-by-property
  "Find blocks with specific properties"
  [db property-key property-value]
  (d/q '[:find [(pull ?block [*]) ...]
         :in $ ?key ?value
         :where
         [?block :block/properties ?props]
         [(get ?props ?key) ?prop-value]
         [(= ?prop-value ?value)]]
       db property-key property-value))

(defn find-orphaned-pages
  "Find pages with no incoming references"
  [db]
  (let [all-pages (d/q '[:find [?page ...]
                        :where [?page :page/name]]
                      db)
        referenced-pages (d/q '[:find [?page ...]
                               :where [?block :block/refs ?page]]
                             db)]
    (remove (set referenced-pages) all-pages)))

(defn get-most-referenced-pages
  "Get pages sorted by number of references"
  [db limit]
  (let [page-ref-counts (d/q '[:find ?page (count ?block)
                              :where
                              [?block :block/refs ?page]]
                            db)]
    (->> page-ref-counts
         (sort-by second >)
         (take limit)
         (mapv (fn [[page-id count]]
                {:page (d/entity db page-id)
                 :ref-count count})))))

(defn find-related-pages
  "Find pages related to a given page through shared references"
  [db page-name similarity-threshold]
  (let [target-page (d/entity db [:page/name page-name])
        target-refs (d/q '[:find [?ref ...]
                          :in $ ?page
                          :where
                          [?block :block/page ?page]
                          [?block :block/refs ?ref]]
                        db (:db/id target-page))
        target-ref-set (set target-refs)]
    
    (when (seq target-refs)
      (let [candidate-pages (d/q '[:find [?other-page ...]
                                  :in $ [?ref ...]
                                  :where
                                  [?block :block/refs ?ref]
                                  [?block :block/page ?other-page]]
                                db target-refs)
            similarity-scores (for [candidate-page candidate-pages
                                   :when (not= candidate-page (:db/id target-page))]
                               (let [candidate-refs (d/q '[:find [?ref ...]
                                                           :in $ ?page
                                                           :where
                                                           [?block :block/page ?page]
                                                           [?block :block/refs ?ref]]
                                                         db candidate-page)
                                     candidate-ref-set (set candidate-refs)
                                     intersection (set/intersection target-ref-set candidate-ref-set)
                                     union (set/union target-ref-set candidate-ref-set)
                                     jaccard-similarity (if (empty? union)
                                                        0
                                                        (/ (count intersection) (count union)))]
                                 {:page (d/entity db candidate-page)
                                  :similarity jaccard-similarity
                                  :shared-refs (count intersection)}))]
        (->> similarity-scores
             (filter #(>= (:similarity %) similarity-threshold))
             (sort-by :similarity >))))))

;; =============================================================================
;; File System Integration
;; =============================================================================

(defn parse-markdown-file
  "Parse a markdown file into blocks"
  [file-content file-path]
  (let [lines (str/split-lines file-content)
        file-entity {:file/path file-path
                     :file/content file-content
                     :file/last-modified-at (js/Date.)
                     :file/size (count file-content)}]
    
    (loop [lines lines
           blocks []
           current-page nil
           indent-stack []]
      (if (empty? lines)
        {:file file-entity
         :page current-page
         :blocks blocks}
        
        (let [line (first lines)
              remaining-lines (rest lines)
              trimmed-line (str/trim line)
              indent-level (- (count line) (count (str/triml line)))]
          
          (cond
            ;; Page title (# Header)
            (str/starts-with? trimmed-line "# ")
            (let [page-name (str/replace trimmed-line #"^# " "")
                  page {:page/name page-name
                        :page/original-name page-name
                        :page/file file-entity
                        :page/created-at (js/Date.)
                        :page/updated-at (js/Date.)}]
              (recur remaining-lines blocks page []))
            
            ;; Block content (- Item)
            (and (not (empty? trimmed-line))
                 (or (str/starts-with? trimmed-line "- ")
                     (str/starts-with? trimmed-line "* ")
                     (not (empty? trimmed-line))))
            (let [content (if (str/starts-with? trimmed-line "- ")
                           (str/replace trimmed-line #"^- " "")
                           trimmed-line)
                  block (create-block content {:page current-page
                                              :file file-entity
                                              :indent-level indent-level})]
              (recur remaining-lines (conj blocks block) current-page indent-stack))
            
            ;; Empty line or other content
            :else
            (recur remaining-lines blocks current-page indent-stack)))))))

(defn serialize-blocks-to-markdown
  "Convert blocks back to markdown format"
  [db page-name]
  (let [page (d/entity db [:page/name page-name])
        blocks (d/q '[:find [(pull ?block [*]) ...]
                     :in $ ?page
                     :where [?block :block/page ?page]
                     :missing-clause [?block :block/parent]]
                   db (:db/id page))]
    
    (str "# " page-name "\n\n"
         (->> blocks
              (sort-by :block/created-at)
              (map #(block-to-markdown-line % db 0))
              (str/join "\n")))))

(defn block-to-markdown-line
  "Convert a single block to markdown format with proper indentation"
  [block db indent-level]
  (let [indent (str/join (repeat indent-level "  "))
        content (:block/content block)
        children (get-block-children db (:block/uuid block))]
    
    (str indent "- " content
         (when (seq children)
           (str "\n"
                (->> children
                     (sort-by :block/created-at)
                     (map #(block-to-markdown-line % db (inc indent-level)))
                     (str/join "\n")))))))

;; =============================================================================
;; Real-time Collaboration & Synchronization
;; =============================================================================

(defprotocol CollaborationManager
  "Protocol for handling real-time collaboration"
  (join-session [this session-id user-id])
  (leave-session [this session-id user-id])
  (broadcast-change [this session-id change])
  (apply-remote-change [this change])
  (resolve-conflict [this local-change remote-change]))

(defrecord WebRTCCollaborationManager [sessions change-channel]
  CollaborationManager
  
  (join-session [this session-id user-id]
    (swap! sessions update session-id (fnil conj #{}) user-id)
    (go (>! change-channel {:type :user-joined
                           :session-id session-id
                           :user-id user-id})))
  
  (leave-session [this session-id user-id]
    (swap! sessions update session-id (fnil disj #{}) user-id)
    (go (>! change-channel {:type :user-left
                           :session-id session-id  
                           :user-id user-id})))
  
  (broadcast-change [this session-id change]
    (when-let [users (get @sessions session-id)]
      (doseq [user-id users]
        (go (>! change-channel (assoc change 
                                     :session-id session-id
                                     :target-user user-id))))))
  
  (apply-remote-change [this change]
    ;; Apply operational transform to resolve conflicts
    (let [transformed-change (transform-operation change)]
      (case (:type transformed-change)
        :block-insert (handle-remote-block-insert transformed-change)
        :block-update (handle-remote-block-update transformed-change)
        :block-delete (handle-remote-block-delete transformed-change)
        :block-move (handle-remote-block-move transformed-change))))
  
  (resolve-conflict [this local-change remote-change]
    ;; Implement operational transform algorithm
    (let [local-timestamp (:timestamp local-change)
          remote-timestamp (:timestamp remote-change)]
      (if (< local-timestamp remote-timestamp)
        ;; Remote change wins, transform local change
        (transform-against-remote local-change remote-change)
        ;; Local change wins, transform remote change
        (transform-against-local remote-change local-change)))))

(defn transform-operation
  "Apply operational transform to make changes consistent"
  [operation]
  ;; Simplified operational transform - production would be more complex
  (case (:type operation)
    :text-insert
    (let [position (:position operation)
          text (:text operation)
          concurrent-ops (:concurrent-operations operation)]
      (assoc operation 
             :position (adjust-position position concurrent-ops)))
    
    :text-delete
    (let [position (:position operation)
          length (:length operation)
          concurrent-ops (:concurrent-operations operation)]
      (assoc operation 
             :position (adjust-position position concurrent-ops)
             :length (adjust-length length position concurrent-ops)))
    
    operation))

(defn handle-remote-block-insert [change]
  ;; Handle remote block insertion with conflict resolution
  )

(defn handle-remote-block-update [change] 
  ;; Handle remote block updates with operational transforms
  )

(defn handle-remote-block-delete [change]
  ;; Handle remote block deletion with validation
  )

(defn handle-remote-block-move [change]
  ;; Handle remote block movement with hierarchy validation
  )

;; =============================================================================
;; Plugin Architecture & Extension System
;; =============================================================================

(defprotocol PluginManager
  "Protocol for managing Logseq plugins"
  (register-plugin [this plugin-config])
  (unregister-plugin [this plugin-id])
  (execute-plugin-command [this plugin-id command args])
  (get-plugin-api [this plugin-id]))

(defrecord LogseqPluginManager [plugins api-registry sandbox]
  PluginManager
  
  (register-plugin [this plugin-config]
    (let [plugin-id (:id plugin-config)
          plugin-api (create-plugin-api plugin-config)
          sandboxed-env (create-sandbox plugin-config)]
      (swap! plugins assoc plugin-id {:config plugin-config
                                      :api plugin-api
                                      :sandbox sandboxed-env
                                      :state (atom {})})
      (swap! api-registry assoc plugin-id plugin-api)))
  
  (unregister-plugin [this plugin-id]
    (when-let [plugin (get @plugins plugin-id)]
      (cleanup-plugin plugin)
      (swap! plugins dissoc plugin-id)
      (swap! api-registry dissoc plugin-id)))
  
  (execute-plugin-command [this plugin-id command args]
    (when-let [plugin (get @plugins plugin-id)]
      (let [sandbox (:sandbox plugin)
            api (:api plugin)]
        (execute-in-sandbox sandbox command args api))))
  
  (get-plugin-api [this plugin-id]
    (get @api-registry plugin-id)))

(defn create-plugin-api
  "Create restricted API for plugin use"
  [plugin-config]
  {:db {:query (partial secure-db-query plugin-config)
        :transact (partial secure-db-transact plugin-config)}
   :ui {:show-message #(js/alert %)
        :create-element (partial safe-create-element plugin-config)}
   :editor {:insert-block (partial secure-insert-block plugin-config)
            :update-block (partial secure-update-block plugin-config)}
   :settings {:get (partial get-plugin-setting plugin-config)
              :set (partial set-plugin-setting plugin-config)}})

(defn create-sandbox
  "Create isolated execution environment for plugins"
  [plugin-config]
  ;; Simplified sandbox - production would use more sophisticated isolation
  {:allowed-globals #{"console" "JSON" "Date" "Math"}
   :allowed-apis (:permissions plugin-config)
   :timeout 5000 ; 5 second execution timeout
   :memory-limit (* 50 1024 1024)}) ; 50MB memory limit

(defn execute-in-sandbox
  "Execute plugin code in sandboxed environment"
  [sandbox command args api]
  (try
    ;; This would use a proper JavaScript VM in production
    (let [result (apply command args)]
      {:success true :result result})
    (catch js/Error e
      {:success false :error (.-message e)})))

;; Plugin security functions
(defn secure-db-query [plugin-config query]
  (when (plugin-has-permission? plugin-config :db-read)
    ;; Validate and execute query with restrictions
    ))

(defn secure-db-transact [plugin-config tx-data]
  (when (plugin-has-permission? plugin-config :db-write)
    ;; Validate transaction data and execute
    ))

(defn plugin-has-permission? [plugin-config permission]
  (contains? (set (:permissions plugin-config)) permission))

;; =============================================================================
;; Graph Visualization & Analysis
;; =============================================================================

(defn calculate-page-rank
  "Calculate PageRank scores for pages in the graph"
  [db damping-factor max-iterations]
  (let [pages (d/q '[:find [?page ...]
                    :where [?page :page/name]]
                  db)
        page-count (count pages)
        initial-score (/ 1.0 page-count)
        
        ;; Get outlinks for each page
        outlinks (into {} 
                      (map (fn [page]
                             [page (d/q '[:find [?target ...]
                                         :in $ ?source
                                         :where
                                         [?block :block/page ?source]
                                         [?block :block/refs ?target]]
                                       db page)]))
                      pages)
        
        ;; Initialize scores
        initial-scores (into {} (map #(vector % initial-score) pages))]
    
    (loop [iteration 0
           scores initial-scores]
      (if (>= iteration max-iterations)
        scores
        (let [new-scores
              (into {}
                    (map (fn [page]
                           (let [inlink-contribution
                                 (reduce +
                                        (for [other-page pages
                                              :when (contains? (set (get outlinks other-page)) page)]
                                          (let [outlink-count (count (get outlinks other-page 0))]
                                            (if (> outlink-count 0)
                                              (/ (get scores other-page) outlink-count)
                                              0))))
                                 new-score (+ (* (- 1 damping-factor) (/ 1.0 page-count))
                                             (* damping-factor inlink-contribution))]
                             [page new-score]))
                         pages))]
          (recur (inc iteration) new-scores))))))

(defn detect-communities
  "Detect communities in the page graph using modularity optimization"
  [db]
  (let [graph (get-page-graph db)
        nodes (:nodes graph)
        edges (:edges graph)
        
        ;; Initialize each node in its own community
        initial-communities (into {} (map-indexed (fn [idx node]
                                                   [(:page/name node) idx])
                                                 nodes))
        
        ;; Calculate modularity for current community assignment
        modularity (fn [communities]
                    (calculate-modularity nodes edges communities))]
    
    ;; Simplified community detection - production would use Louvain algorithm
    (loop [communities initial-communities
           current-modularity (modularity initial-communities)
           improved? true]
      (if-not improved?
        communities
        (let [best-move (find-best-community-move nodes edges communities)
              new-communities (if best-move
                               (apply-community-move communities best-move)
                               communities)
              new-modularity (modularity new-communities)]
          (recur new-communities
                new-modularity
                (> new-modularity current-modularity)))))))

(defn calculate-modularity
  "Calculate modularity score for community assignment"
  [nodes edges communities]
  (let [total-edges (count edges)
        community-groups (group-by second communities)]
    ;; Simplified modularity calculation
    (reduce + 
           (for [[community members] community-groups]
             (let [internal-edges (count-internal-edges edges members)
                   expected-edges (calculate-expected-edges nodes edges members total-edges)]
               (- (/ internal-edges total-edges)
                  (Math/pow (/ expected-edges total-edges) 2)))))))

;; =============================================================================
;; Performance Optimization & Caching
;; =============================================================================

(def query-cache (atom {}))
(def cache-ttl (* 5 60 1000)) ; 5 minutes

(defn cached-query
  "Execute query with caching"
  [db query args cache-key]
  (let [now (js/Date.)
        cached-result (get @query-cache cache-key)]
    (if (and cached-result
             (< (- (.getTime now) (.getTime (:timestamp cached-result)))
                cache-ttl))
      (:result cached-result)
      (let [result (d/q query db args)]
        (swap! query-cache assoc cache-key {:result result
                                           :timestamp now})
        result))))

(defn invalidate-cache
  "Invalidate cache entries matching pattern"
  [pattern]
  (swap! query-cache 
         (fn [cache]
           (into {} (remove (fn [[k v]] (re-find pattern (str k))) cache)))))

(defn optimize-large-graph-rendering
  "Optimize rendering of large graphs using clustering and LOD"
  [graph zoom-level viewport]
  (cond
    ;; High zoom - show all details
    (> zoom-level 2.0)
    graph
    
    ;; Medium zoom - cluster small nodes
    (> zoom-level 0.5)
    (cluster-nodes graph {:min-cluster-size 3
                         :max-clusters 100})
    
    ;; Low zoom - aggressive clustering
    :else
    (cluster-nodes graph {:min-cluster-size 10
                         :max-clusters 20})))

(defn cluster-nodes
  "Cluster nodes for performance optimization"
  [graph clustering-options]
  (let [nodes (:nodes graph)
        edges (:edges graph)
        clusters (detect-node-clusters nodes edges clustering-options)]
    {:nodes (create-cluster-nodes clusters)
     :edges (create-cluster-edges edges clusters)}))

;; =============================================================================
;; Integration Examples & Usage Patterns
;; =============================================================================

(defn demonstration-workflow
  "Comprehensive demonstration of Logseq's block system capabilities"
  []
  (let [db (d/create-conn logseq-schema)]
    
    ;; 1. Create some example pages and blocks
    (println "=== Creating Knowledge Base ===")
    
    (let [programming-page (create-page-if-not-exists db "Programming")
          clojure-page (create-page-if-not-exists db "ClojureScript")
          
          intro-block (create-block 
                      "Programming is the art of [[Problem Solving]] with code."
                      {:page programming-page})
          
          clojure-block (create-block
                        "[[ClojureScript]] is a dialect of [[Clojure]] that compiles to JavaScript."
                        {:page programming-page
                         :parent intro-block})
          
          benefits-block (create-block
                         "Benefits of functional programming: #immutability #composability"
                         {:page clojure-page})]
      
      (insert-block db intro-block)
      (insert-block db clojure-block) 
      (insert-block db benefits-block)
      
      ;; 2. Demonstrate querying and navigation
      (println "\n=== Querying Knowledge Graph ===")
      
      (let [all-references (get-page-references db "ClojureScript")
            backlinks (get-page-backlinks db "ClojureScript")
            search-results (search-blocks db "functional")]
        
        (println "ClojureScript references:" (count all-references))
        (println "Backlinks:" (map :page/name backlinks))
        (println "Functional programming mentions:" (count search-results)))
      
      ;; 3. Demonstrate graph analysis
      (println "\n=== Graph Analysis ===")
      
      (let [page-rank (calculate-page-rank db 0.85 10)
            communities (detect-communities db)
            orphaned-pages (find-orphaned-pages db)]
        
        (println "Page rankings:" 
                (take 5 (sort-by second > page-rank)))
        (println "Community structure:" 
                (count (distinct (vals communities))))
        (println "Orphaned pages:" (count orphaned-pages)))
      
      ;; 4. Demonstrate file system integration
      (println "\n=== File System Integration ===")
      
      (let [markdown-content (serialize-blocks-to-markdown db "Programming")
            parsed-data (parse-markdown-file markdown-content "programming.md")]
        
        (println "Markdown export length:" (count markdown-content))
        (println "Parsed blocks:" (count (:blocks parsed-data))))
      
      ;; 5. Demonstrate plugin system
      (println "\n=== Plugin System ===")
      
      (let [plugin-manager (->LogseqPluginManager (atom {}) (atom {}) nil)
            sample-plugin {:id "sample-plugin"
                          :name "Sample Plugin"
                          :version "1.0.0"
                          :permissions [:db-read :ui-write]}]
        
        (register-plugin plugin-manager sample-plugin)
        (println "Plugin registered:" (:id sample-plugin))
        (println "Available APIs:" 
                (keys (get-plugin-api plugin-manager "sample-plugin"))))
      
      (println "\n=== Demonstration Complete ===")
      {:status :success
       :message "Logseq block system demonstration completed successfully"})))

;; =============================================================================
;; Performance Benchmarking & Monitoring
;; =============================================================================

(defn benchmark-operations
  "Benchmark various operations for performance analysis"
  [db num-operations]
  (let [start-time (js/Date.)]
    
    ;; Benchmark block creation
    (dotimes [i num-operations]
      (let [block (create-block (str "Test block " i))]
        (insert-block db block)))
    
    (let [creation-time (- (.getTime (js/Date.)) (.getTime start-time))]
      
      ;; Benchmark querying
      (let query-start (js/Date.)]
        (dotimes [i 100]
          (search-blocks db "Test"))
        
        (let [query-time (- (.getTime (js/Date.)) (.getTime query-start))
              graph (get-page-graph db)]
          
          {:block-creation {:operations num-operations
                           :time-ms creation-time
                           :ops-per-second (/ num-operations (/ creation-time 1000))}
           :query-performance {:operations 100
                              :time-ms query-time
                              :ops-per-second (/ 100 (/ query-time 1000))}
           :graph-stats {:nodes (count (:nodes graph))
                        :edges (count (:edges graph))}}))))

(defn monitor-memory-usage
  "Monitor memory usage patterns"
  []
  (when (and js/performance js/performance.memory)
    {:used-js-heap-size (.-usedJSHeapSize js/performance.memory)
     :total-js-heap-size (.-totalJSHeapSize js/performance.memory)
     :js-heap-size-limit (.-jsHeapSizeLimit js/performance.memory)}))

;; Run demonstration when this namespace is loaded
(comment
  (demonstration-workflow)
  
  ;; Example of plugin development
  (def my-plugin
    {:id "custom-block-processor"
     :name "Custom Block Processor"
     :version "1.0.0"
     :permissions [:db-read :db-write :ui-write]
     :commands {:process-blocks (fn [blocks options]
                                 (map #(update % :content str/upper-case) blocks))}})
  
  ;; Performance testing  
  (let [db (d/create-conn logseq-schema)
        results (benchmark-operations db 1000)]
    (println "Performance results:" results)))
