; Athens Research Datascript Query Examples
; 
; This file demonstrates how Athens Research uses Datascript
; for graph-based knowledge management
; 
; Key concepts:
; - Graph database queries
; - Bi-directional linking
; - Block hierarchy traversal
; - Content search and filtering

(ns athens.examples.datascript-queries
  (:require [datascript.core :as d]
            [athens.db :as db]
            [clojure.string :as string]))

;; =============================================================================
;; Schema Definition
;; =============================================================================

(def athens-schema
  "Athens Research database schema - models pages, blocks, and relationships"
  {:page/title       {:db/unique :db.unique/identity}
   :page/uid         {:db/unique :db.unique/identity}
   :page/created     {}
   :page/modified    {}
   
   :block/uid        {:db/unique :db.unique/identity}
   :block/string     {}
   :block/order      {}
   :block/open       {}
   :block/children   {:db/valueType :db.type/ref
                      :db/cardinality :db.cardinality/many}
   :block/page       {:db/valueType :db.type/ref}
   :block/refs       {:db/valueType :db.type/ref
                      :db/cardinality :db.cardinality/many}
   :block/created    {}
   :block/modified   {}})

;; =============================================================================
;; Sample Data
;; =============================================================================

(def sample-data
  "Sample Athens Research database for demonstration"
  [;; Pages
   {:page/title "My Daily Notes"
    :page/uid "daily-notes-123"
    :page/created #inst "2023-01-01"}
   
   {:page/title "ClojureScript Learning"
    :page/uid "cljs-learning-456" 
    :page/created #inst "2023-01-02"}
   
   {:page/title "Athens Research"
    :page/uid "athens-research-789"
    :page/created #inst "2023-01-03"}
   
   ;; Blocks with hierarchy
   {:block/uid "block-001"
    :block/string "Today I learned about [[ClojureScript Learning]]"
    :block/page [:page/uid "daily-notes-123"]
    :block/refs [[:page/uid "cljs-learning-456"]]
    :block/order 1
    :block/open true}
   
   {:block/uid "block-002"
    :block/string "ClojureScript is a functional language that compiles to JavaScript"
    :block/page [:page/uid "cljs-learning-456"]
    :block/order 1
    :block/open true}
   
   {:block/uid "block-003"
    :block/string "Key features include:"
    :block/page [:page/uid "cljs-learning-456"]
    :block/children [[:block/uid "block-004"] [:block/uid "block-005"]]
    :block/order 2
    :block/open true}
   
   {:block/uid "block-004"
    :block/string "Immutable data structures"
    :block/page [:page/uid "cljs-learning-456"]
    :block/order 1
    :block/open true}
   
   {:block/uid "block-005"
    :block/string "Functional programming paradigms"
    :block/page [:page/uid "cljs-learning-456"]
    :block/order 2
    :block/open true}
   
   {:block/uid "block-006"
    :block/string "[[Athens Research]] uses ClojureScript extensively"
    :block/page [:page/uid "cljs-learning-456"]
    :block/refs [[:page/uid "athens-research-789"]]
    :block/order 3
    :block/open true}
   
   {:block/uid "block-007"
    :block/string "Athens Research is an open-source knowledge management tool"
    :block/page [:page/uid "athens-research-789"]
    :block/order 1
    :block/open true}])

;; =============================================================================
;; Database Connection Setup
;; =============================================================================

(defn create-sample-db
  "Create a sample Athens database for testing queries"
  []
  (let [conn (d/create-conn athens-schema)]
    (d/transact! conn sample-data)
    conn))

;; =============================================================================
;; Basic Queries
;; =============================================================================

(defn get-all-pages
  "Find all pages in the database"
  [db]
  (d/q '[:find ?title ?uid ?created
         :where 
         [?e :page/title ?title]
         [?e :page/uid ?uid]
         [?e :page/created ?created]]
       db))

(defn get-page-by-title
  "Find a specific page by title"
  [db title]
  (d/q '[:find (pull ?e [*])
         :in $ ?title
         :where [?e :page/title ?title]]
       db title))

(defn get-blocks-on-page
  "Find all blocks on a specific page"
  [db page-title]
  (d/q '[:find ?uid ?string ?order
         :in $ ?page-title
         :where
         [?page :page/title ?page-title]
         [?block :block/page ?page]
         [?block :block/uid ?uid]
         [?block :block/string ?string]
         [?block :block/order ?order]]
       db page-title))

;; =============================================================================
;; Hierarchy Queries
;; =============================================================================

(defn get-block-children
  "Find all direct children of a block"
  [db block-uid]
  (d/q '[:find ?child-uid ?child-string ?child-order
         :in $ ?parent-uid
         :where
         [?parent :block/uid ?parent-uid]
         [?parent :block/children ?child]
         [?child :block/uid ?child-uid]
         [?child :block/string ?child-string]
         [?child :block/order ?child-order]]
       db block-uid))

(defn get-block-tree
  "Recursively get a block and all its descendants"
  [db block-uid]
  (letfn [(get-descendants [uid depth]
            (let [block (d/entity db [:block/uid uid])
                  children (sort-by :block/order (:block/children block))]
              {:block/uid uid
               :block/string (:block/string block)
               :block/order (:block/order block)
               :block/depth depth
               :block/children (mapv #(get-descendants (:block/uid %) (inc depth))
                                   children)}))]
    (get-descendants block-uid 0)))

(defn find-orphaned-blocks
  "Find blocks that don't belong to any page or parent block"
  [db]
  (d/q '[:find ?uid ?string
         :where
         [?e :block/uid ?uid]
         [?e :block/string ?string]
         (not [?e :block/page _])
         (not [_ :block/children ?e])]
       db))

;; =============================================================================
;; Bi-directional Link Queries
;; =============================================================================

(defn get-page-references
  "Find all blocks that reference a specific page"
  [db page-title]
  (d/q '[:find ?block-uid ?block-string ?source-page-title
         :in $ ?target-title
         :where
         [?target-page :page/title ?target-title]
         [?block :block/refs ?target-page]
         [?block :block/uid ?block-uid]
         [?block :block/string ?block-string]
         [?block :block/page ?source-page]
         [?source-page :page/title ?source-page-title]]
       db page-title))

(defn get-backlinks-for-page
  "Get all pages that link to the target page"
  [db target-page-title]
  (d/q '[:find ?source-page-title (count ?block-uid)
         :in $ ?target-title
         :where
         [?target-page :page/title ?target-title]
         [?block :block/refs ?target-page]
         [?block :block/uid ?block-uid]
         [?block :block/page ?source-page]
         [?source-page :page/title ?source-page-title]]
       db target-page-title))

(defn find-connected-pages
  "Find pages that are mutually connected (bidirectional references)"
  [db]
  (d/q '[:find ?page1-title ?page2-title
         :where
         [?page1 :page/title ?page1-title]
         [?page2 :page/title ?page2-title]
         [?block1 :block/page ?page1]
         [?block1 :block/refs ?page2]
         [?block2 :block/page ?page2]
         [?block2 :block/refs ?page1]
         [(< ?page1-title ?page2-title)]] ; Avoid duplicates
       db))

;; =============================================================================
;; Search and Filter Queries
;; =============================================================================

(defn search-blocks-by-text
  "Search for blocks containing specific text"
  [db search-term]
  (d/q '[:find ?uid ?string ?page-title
         :in $ ?search
         :where
         [?e :block/uid ?uid]
         [?e :block/string ?string]
         [?e :block/page ?page]
         [?page :page/title ?page-title]
         [(clojure.string/includes? ?string ?search)]]
       db search-term))

(defn search-pages-by-title
  "Search for pages with titles containing specific text"
  [db search-term]
  (d/q '[:find ?title ?uid
         :in $ ?search
         :where
         [?e :page/title ?title]
         [?e :page/uid ?uid]
         [(clojure.string/includes? ?title ?search)]]
       db search-term))

(defn find-recent-pages
  "Find pages created within the last N days"
  [db days-ago]
  (let [cutoff-date (-> (js/Date.)
                       (.getTime)
                       (- (* days-ago 24 60 60 1000))
                       (js/Date.))]
    (d/q '[:find ?title ?created
           :in $ ?cutoff
           :where
           [?e :page/title ?title]
           [?e :page/created ?created]
           [(> ?created ?cutoff)]]
         db cutoff-date)))

;; =============================================================================
;; Graph Analysis Queries
;; =============================================================================

(defn get-page-connectivity-score
  "Calculate how connected a page is (number of inbound + outbound refs)"
  [db page-title]
  (let [inbound (d/q '[:find (count ?block)
                       :in $ ?title
                       :where
                       [?page :page/title ?title]
                       [?block :block/refs ?page]]
                     db page-title)
        outbound (d/q '[:find (count ?ref)
                        :in $ ?title
                        :where
                        [?page :page/title ?title]
                        [?block :block/page ?page]
                        [?block :block/refs ?ref]]
                      db page-title)]
    {:page/title page-title
     :inbound-refs (or (ffirst inbound) 0)
     :outbound-refs (or (ffirst outbound) 0)
     :total-connectivity (+ (or (ffirst inbound) 0)
                           (or (ffirst outbound) 0))}))

(defn find-hub-pages
  "Find pages with the most connections (potential hub pages)"
  [db limit]
  (->> (d/q '[:find ?title
              :where [_ :page/title ?title]]
            db)
       (map first)
       (map #(get-page-connectivity-score db %))
       (sort-by :total-connectivity >)
       (take limit)))

(defn find-isolated-pages
  "Find pages with no connections (orphaned pages)"
  [db]
  (d/q '[:find ?title
         :where
         [?page :page/title ?title]
         (not [?block :block/refs ?page])
         (not [?block :block/page ?page
               :block/refs _])]
       db))

;; =============================================================================
;; Advanced Graph Traversal
;; =============================================================================

(defn find-shortest-path
  "Find shortest path between two pages through references"
  [db start-page end-page]
  (letfn [(get-neighbors [page-title]
            (->> (d/q '[:find ?neighbor-title
                        :in $ ?title
                        :where
                        [?page :page/title ?title]
                        [?block :block/page ?page]
                        [?block :block/refs ?neighbor]
                        [?neighbor :page/title ?neighbor-title]]
                      db page-title)
                 (map first)))
          
          (bfs [start end]
            (loop [queue [[start]]
                   visited #{start}]
              (when (seq queue)
                (let [path (first queue)
                      current (last path)]
                  (if (= current end)
                    path
                    (let [neighbors (->> (get-neighbors current)
                                        (remove visited))
                          new-paths (map #(conj path %) neighbors)
                          new-visited (into visited neighbors)]
                      (recur (concat (rest queue) new-paths)
                             new-visited)))))))]
    
    (bfs start-page end-page)))

;; =============================================================================
;; Utility Functions
;; =============================================================================

(defn parse-page-references
  "Extract page references from block text (e.g., [[Page Name]])"
  [text]
  (re-seq #"\[\[([^\]]+)\]\]" text))

(defn create-bi-directional-link
  "Create a transaction that adds bi-directional links between blocks"
  [db source-block-uid target-page-title]
  (let [target-page-id [:page/title target-page-title]
        source-block-id [:block/uid source-block-uid]]
    [{:db/id source-block-id
      :block/refs target-page-id}]))

(defn update-block-references
  "Update block references based on its content"
  [db block-uid new-content]
  (let [page-refs (map second (parse-page-references new-content))
        page-entities (map #(vector :page/title %) page-refs)]
    [{:db/id [:block/uid block-uid]
      :block/string new-content
      :block/refs page-entities}]))

;; =============================================================================
;; Example Usage and Tests
;; =============================================================================

(defn run-example-queries
  "Run example queries to demonstrate Athens Research patterns"
  []
  (let [conn (create-sample-db)
        db @conn]
    
    (println "=== All Pages ===")
    (doseq [[title uid created] (get-all-pages db)]
      (println (str "• " title " (" uid ")")))
    
    (println "\n=== Blocks on ClojureScript Learning Page ===")
    (doseq [[uid string order] (get-blocks-on-page db "ClojureScript Learning")]
      (println (str "  " order ". " string " [" uid "]")))
    
    (println "\n=== Block Hierarchy for block-003 ===")
    (cljs.pprint/pprint (get-block-tree db "block-003"))
    
    (println "\n=== References to ClojureScript Learning ===")
    (doseq [[block-uid block-string source-page] (get-page-references db "ClojureScript Learning")]
      (println (str "• " block-string " (from " source-page ")")))
    
    (println "\n=== Search Results for 'ClojureScript' ===")
    (doseq [[uid string page] (search-blocks-by-text db "ClojureScript")]
      (println (str "• " string " (in " page ")")))
    
    (println "\n=== Hub Pages (by connectivity) ===")
    (doseq [hub (find-hub-pages db 5)]
      (println (str "• " (:page/title hub) " (score: " (:total-connectivity hub) ")")))))

;; Run the examples when this namespace is loaded
(comment
  (run-example-queries))

;; =============================================================================
;; Integration with Re-frame Events
;; =============================================================================

(comment
  "Example Re-frame event handlers using these queries"
  
  (rf/reg-event-fx
    :search/text
    (fn [{:keys [db]} [_ search-term]]
      (let [results (search-blocks-by-text @athens.db/dsdb search-term)]
        {:db (assoc db :search/results results)})))
  
  (rf/reg-event-fx
    :graph/find-connections
    (fn [{:keys [db]} [_ page-title]]
      (let [connections (get-page-references @athens.db/dsdb page-title)]
        {:db (assoc db :graph/connections connections)})))
  
  (rf/reg-sub
    :search/results
    (fn [db _]
      (:search/results db))))
