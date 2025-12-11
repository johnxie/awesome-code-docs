---
layout: default
title: "Chapter 3: Schema Design"
nav_order: 3
has_children: false
parent: "Athens Research Knowledge Graph"
---

# Chapter 3: Schema Design

> Modeling blocks, pages, and relationships in Athens Research

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- How to design schemas for graph-based knowledge systems
- Entity relationships and cardinalities in Datascript
- Migration strategies for evolving schemas
- Performance implications of schema design decisions
- Best practices for knowledge graph data modeling

## 🏗️ Schema Design Principles

### **Graph-First Thinking**

Unlike relational databases, graph databases prioritize relationships:

```clojure
;; Traditional relational approach
{:tables
 {:users {:columns {:id :integer, :name :string}}
  :posts {:columns {:id :integer, :user_id :integer, :title :string}}
  :comments {:columns {:id :integer, :post_id :integer, :user_id :integer}}}}

;; Graph approach - relationships are first-class
{:entities
 {:user {:properties {:name :string}}
  :post {:properties {:title :string, :content :string}}
  :comment {:properties {:text :string}}}

 :relationships
 {:author {:from :post, :to :user, :cardinality :many-to-one}
  :comments {:from :post, :to :comment, :cardinality :one-to-many}
  :commenter {:from :comment, :to :user, :cardinality :many-to-one}}}
```

### **Entity-Centric Design**

In Athens, everything revolves around entities and their connections:

```clojure
;; Core entity types
(def entity-types
  {:block     {:description "Atomic unit of content"}
   :page      {:description "Collection of blocks"}
   :reference {:description "Link between entities"}
   :user      {:description "System user"}
   :file      {:description "Attached file or image"}})
```

## 📄 Block Entity Design

### **Block Schema Definition**

```clojure
;; Complete block schema
(def block-schema
  {;; Identity
   :block/uuid {:db/unique :db.unique/identity
                :db/type :db.type/uuid
                :db/doc "Unique identifier for the block"}

   ;; Content
   :block/string {:db/type :db.type/string
                  :db/doc "Text content of the block"}

   ;; Structure
   :block/order {:db/type :db.type/long
                 :db/doc "Position among sibling blocks"}

   :block/level {:db/type :db.type/long
                 :db/doc "Nesting level (computed)"}

   ;; Relationships
   :block/children {:db/type :db.type/ref
                    :db/cardinality :db.cardinality/many
                    :db/doc "Child blocks"}

   :block/parent {:db/type :db.type/ref
                  :db/cardinality :db.cardinality/one
                  :db/doc "Parent block (inverse of children)"}

   ;; References
   :block/refs {:db/type :db.type/ref
                :db/cardinality :db.cardinality/many
                :db/doc "Pages referenced by this block"}

   :block/_refs {:db/type :db.type/ref
                 :db/cardinality :db.cardinality/many
                 :db/doc "Blocks that reference this page (backlinks)"}

   ;; Metadata
   :block/created-at {:db/type :db.type/instant
                      :db/doc "Creation timestamp"}

   :block/updated-at {:db/type :db.type/instant
                      :db/doc "Last modification timestamp"}

   :block/created-by {:db/type :db.type/ref
                      :db/cardinality :db.cardinality/one
                      :db/doc "User who created this block"}

   ;; UI State
   :block/collapsed? {:db/type :db.type/boolean
                      :db/doc "Whether children are collapsed in UI"}

   :block/editing? {:db/type :db.type/boolean
                    :db/doc "Whether block is in edit mode"}})
```

### **Block Relationships**

```clojure
;; Block relationship patterns

;; Parent-child hierarchy
{:block/uuid #uuid "parent-uuid"
 :block/children [#uuid "child1-uuid" #uuid "child2-uuid"]}

;; References to pages
{:block/uuid #uuid "block-uuid"
 :block/refs ["Machine Learning" "Artificial Intelligence"]}

;; Inverse references (backlinks)
{:page/title "Machine Learning"
 :page/_refs [#uuid "block1-uuid" #uuid "block2-uuid"]}
```

### **Block Lifecycle**

```clojure
;; Block creation
(defn create-block [content & {:keys [parent order]}]
  (let [block-uuid (d/squuid)]
    {:block/uuid block-uuid
     :block/string content
     :block/order (or order 0)
     :block/parent parent
     :block/created-at (js/Date.)
     :block/children []}))

;; Block updates
(defn update-block-content [block-uuid new-content]
  {:block/uuid block-uuid
   :block/string new-content
   :block/updated-at (js/Date.)})

;; Block deletion (soft delete)
(defn delete-block [block-uuid]
  {:block/uuid block-uuid
   :block/deleted? true
   :block/deleted-at (js/Date.)})
```

## 📄 Page Entity Design

### **Page Schema Definition**

```clojure
;; Complete page schema
(def page-schema
  {;; Identity
   :page/uuid {:db/unique :db.unique/identity
               :db/type :db.type/uuid
               :db/doc "Unique identifier for the page"}

   :page/title {:db/unique :db.unique/identity
                :db/type :db.type/string
                :db/doc "Page title (also serves as unique identifier)"}

   ;; Content
   :page/blocks {:db/type :db.type/ref
                 :db/cardinality :db.cardinality/many
                 :db/doc "Blocks that belong to this page"}

   ;; Relationships
   :page/refs {:db/type :db.type/ref
               :db/cardinality :db.cardinality/many
               :db/doc "Pages referenced by this page"}

   :page/_refs {:db/type :db.type/ref
                :db/cardinality :db.cardinality/many
                :db/doc "Pages that reference this page"}

   ;; Metadata
   :page/created-at {:db/type :db.type/instant
                     :db/doc "Page creation timestamp"}

   :page/updated-at {:db/type :db.type/instant
                     :db/doc "Last modification timestamp"}

   :page/created-by {:db/type :db.type/ref
                     :db/cardinality :db.cardinality/one
                     :db/doc "User who created this page"}

   ;; Properties
   :page/properties {:db/type :db.type/ref
                     :db/cardinality :db.cardinality/many
                     :db/doc "Key-value properties for the page"}

   ;; UI State
   :page/collapsed-sections {:db/type :db.type/ref
                            :db/cardinality :db.cardinality/many
                            :db/doc "Which sections are collapsed"}})
```

### **Page-Block Relationships**

```clojure
;; Page with blocks
{:page/uuid #uuid "page-uuid"
 :page/title "Machine Learning"
 :page/blocks [#uuid "block1-uuid" #uuid "block2-uuid" #uuid "block3-uuid"]}

;; Block belongs to page
{:block/uuid #uuid "block1-uuid"
 :block/page #uuid "page-uuid"
 :block/string "Machine learning is..."}
```

### **Page Properties System**

```clojure
;; Page properties (like Logseq properties)
{:page/uuid #uuid "page-uuid"
 :page/properties [{:property/key "type"
                    :property/value "concept"}
                   {:property/key "tags"
                    :property/value ["ml" "ai"]}
                   {:property/key "difficulty"
                    :property/value "intermediate"}]}

;; Property schema
(def property-schema
  {:property/key {:db/type :db.type/keyword}
   :property/value {:db/type :db.type/any} ; Can be string, number, etc.
   :property/page {:db/type :db.type/ref
                   :db/cardinality :db.cardinality/one}})
```

## 🔗 Reference System Design

### **Reference Schema**

```clojure
;; Reference relationship schema
(def reference-schema
  {;; Reference identity
   :reference/id {:db/unique :db.unique/identity
                  :db/type :db.type/uuid
                  :db/doc "Unique identifier for the reference"}

   ;; Source and target
   :reference/from {:db/type :db.type/ref
                    :db/cardinality :db.cardinality/one
                    :db/doc "Block that contains the reference"}

   :reference/to {:db/type :db.type/string
                  :db/cardinality :db.cardinality/one
                  :db/doc "Referenced page title"}

   ;; Context
   :reference/context {:db/type :db.type/string
                       :db/doc "Surrounding text context"}

   :reference/position {:db/type :db.type/long
                        :db/doc "Position in the block text"}

   ;; Metadata
   :reference/created-at {:db/type :db.type/instant
                          :db/doc "When the reference was created"}

   :reference/created-by {:db/type :db.type/ref
                          :db/cardinality :db.cardinality/one
                          :db/doc "User who created the reference"}})
```

### **Reference Processing**

```clojure
;; Reference parsing and creation
(defn parse-references [block-content]
  "Extract [[page]] references from block content"
  (let [ref-pattern #"\[\[([^\]]+)\]\]"
        matches (re-seq ref-pattern block-content)]
    (map (fn [[full-match page-title]]
           {:text page-title
            :position (.indexOf block-content full-match)})
         matches)))

(defn create-references [block-uuid block-content]
  "Create reference entities for a block"
  (let [references (parse-references block-content)]
    (map (fn [ref]
           {:reference/id (d/squuid)
            :reference/from block-uuid
            :reference/to (:text ref)
            :reference/context (extract-context block-content (:position ref))
            :reference/position (:position ref)
            :reference/created-at (js/Date.)})
         references)))

(defn extract-context [content position]
  "Extract surrounding context for a reference"
  (let [start (max 0 (- position 50))
        end (min (count content) (+ position 50))]
    (subs content start end)))
```

### **Unlinked References**

```clojure
;; Unlinked references (pages that don't exist yet)
(def unlinked-schema
  {:unlinked/id {:db/unique :db.unique/identity
                 :db/type :db.type/uuid}

   :unlinked/page {:db/type :db.type/string
                   :db/doc "Title of the non-existent page"}

   :unlinked/block {:db/type :db.type/ref
                    :db/cardinality :db.cardinality/one
                    :db/doc "Block containing the unlinked reference"}

   :unlinked/context {:db/type :db.type/string
                      :db/doc "Context where the reference appears"}

   :unlinked/created-at {:db/type :db.type/instant}

   :unlinked/created-by {:db/type :db.type/ref
                         :db/cardinality :db.cardinality/one}})
```

## 👥 User and Collaboration Schema

### **User Schema**

```clojure
;; User management schema
(def user-schema
  {:user/id {:db/unique :db.unique/identity
             :db/type :db.type/uuid}

   :user/email {:db/unique :db.unique/identity
                :db/type :db.type/string}

   :user/name {:db/type :db.type/string}

   :user/avatar {:db/type :db.type/string
                 :db/doc "Avatar image URL"}

   ;; Preferences
   :user/theme {:db/type :db.type/keyword
                :db/doc "UI theme preference"}

   :user/shortcuts {:db/type :db.type/ref
                    :db/cardinality :db.cardinality/many
                    :db/doc "Custom keyboard shortcuts"}

   ;; Activity tracking
   :user/last-active {:db/type :db.type/instant}

   :user/created-at {:db/type :db.type/instant}

   ;; Collaboration
   :user/shared-pages {:db/type :db.type/ref
                       :db/cardinality :db.cardinality/many
                       :db/doc "Pages shared with this user"}})
```

### **Collaboration Schema**

```clojure
;; Multi-user collaboration schema
(def collaboration-schema
  {;; Page sharing
   :sharing/id {:db/unique :db.unique/identity
                :db/type :db.type/uuid}

   :sharing/page {:db/type :db.type/ref
                  :db/cardinality :db.cardinality/one}

   :sharing/user {:db/type :db.type/ref
                  :db/cardinality :db.cardinality/one}

   :sharing/permission {:db/type :db.type/keyword
                        :db/doc "read, write, admin"}

   :sharing/shared-by {:db/type :db.type/ref
                       :db/cardinality :db.cardinality/one}

   :sharing/shared-at {:db/type :db.type/instant}

   ;; Change tracking
   :change/id {:db/unique :db.unique/identity
               :db/type :db.type/uuid}

   :change/entity {:db/type :db.type/ref
                   :db/cardinality :db.cardinality/one
                   :db/doc "Block or page that was changed"}

   :change/type {:db/type :db.type/keyword
                 :db/doc "create, update, delete"}

   :change/user {:db/type :db.type/ref
                 :db/cardinality :db.cardinality/one}

   :change/timestamp {:db/type :db.type/instant}

   :change/before {:db/type :db.type/any
                   :db/doc "Previous value"}

   :change/after {:db/type :db.type/any
                  :db/doc "New value"}})
```

## 🔄 Schema Evolution

### **Migration Strategy**

```clojure
;; Schema migration framework
(defn create-migration [from-version to-version changes]
  {:id (d/squuid)
   :from-version from-version
   :to-version to-version
   :changes changes
   :created-at (js/Date.)})

(defn apply-migration [conn migration]
  (println "Applying migration:" (:id migration))
  (doseq [change (:changes migration)]
    (apply-schema-change conn change)))

(defn apply-schema-change [conn change]
  (case (:type change)
    :add-attribute
    (d/transact! conn [(merge {:db/id (d/tempid :db.part/db)
                               :db/ident (:attribute change)
                               :db.install/_attribute :db.part/db}
                              (dissoc change :type :attribute))])

    :remove-attribute
    ;; Complex operation - requires data migration
    (remove-attribute-migration conn change)

    :rename-attribute
    (rename-attribute-migration conn change)))

(defn remove-attribute-migration [conn change]
  ;; Strategy: Create new attribute, migrate data, remove old attribute
  (let [old-attr (:attribute change)
        new-attr (keyword (str (name old-attr) "_deprecated"))]
    ;; 1. Create deprecated version
    ;; 2. Migrate existing data
    ;; 3. Update application code
    ;; 4. Eventually remove deprecated attribute
    ))

(defn rename-attribute-migration [conn change]
  (let [old-name (:from change)
        new-name (:to change)]
    ;; Add new attribute
    (apply-schema-change conn {:type :add-attribute
                               :attribute new-name
                               :db/type (:db/type (get-schema old-name))})

    ;; Migrate data
    (let [entities (d/q '[:find ?e ?v
                          :in $ ?attr
                          :where [?e ?attr ?v]]
                        @conn old-name)]
      (doseq [[eid value] entities]
        (d/transact! conn [{:db/id eid new-name value}])))

    ;; Remove old attribute (after application update)
    ;; (apply-schema-change conn {:type :remove-attribute :attribute old-name})
    ))
```

### **Backward Compatibility**

```clojure
;; Version-aware schema handling
(def schema-versions
  {:v1 {:block {:uuid :block/uuid, :string :block/string}}
   :v2 {:block {:uuid :block/uuid, :string :block/string, :order :block/order}}
   :v3 {:block {:uuid :block/uuid, :string :block/string, :order :block/order
                :children :block/children, :refs :block/refs}}})

(defn get-current-schema-version []
  ;; Determine version from database content or metadata
  :v3)

(defn migrate-entity [entity from-version to-version]
  (let [from-schema (get schema-versions from-version)
        to-schema (get schema-versions to-version)]
    ;; Transform entity based on schema differences
    (migrate-entity-structure entity from-schema to-schema)))

(defn migrate-entity-structure [entity from-schema to-schema]
  ;; Handle attribute renames, additions, removals
  (reduce-kv (fn [result old-key new-key]
               (if (contains? entity old-key)
                 (assoc result new-key (get entity old-key))
                 result))
             {}
             (:block from-schema)))
```

## 📊 Query Optimization

### **Indexing Strategy**

```clojure
;; Optimized schema with appropriate indexes
(def optimized-schema
  (merge block-schema
         page-schema
         reference-schema
         {;; Additional indexes for performance
          :block/page {:db/index true
                       :db/doc "Index for fast page-block lookups"}

          :reference/to {:db/index true
                         :db/doc "Index for reference lookups"}

          :page/title {:db/index true
                       :db/doc "Index for page title searches"}

          ;; Compound indexes (Datascript supports these)
          :block/string+order {:db/index true
                               :db/unique false}}))
```

### **Query Performance Patterns**

```clojure
;; Optimized query patterns

;; ✅ Efficient: Uses indexes
(defn get-page-blocks [page-uuid]
  (d/q '[:find (pull ?block [:block/uuid :block/string :block/order])
         :in $ ?page-uuid
         :where [?page :page/uuid ?page-uuid]
                [?page :page/blocks ?block]]
       @conn))

;; ✅ Efficient: Pre-computed relationships
(defn get-block-children [block-uuid]
  (d/q '[:find (pull ?child [:block/uuid :block/string])
         :in $ ?block-uuid
         :where [?block :block/uuid ?block-uuid]
                [?block :block/children ?child]]
       @conn))

;; ✅ Efficient: Batch operations
(defn get-multiple-pages [page-uuids]
  (d/q '[:find ?uuid ?title (pull ?blocks [:block/uuid :block/string])
         :in $ [?uuid ...]
         :where [?page :page/uuid ?uuid]
                [?page :page/title ?title]
                [?page :page/blocks ?blocks]]
       @conn page-uuids))

;; ❌ Inefficient: Full table scan
(defn search-blocks-naive [search-term]
  (let [all-blocks (d/q '[:find ?e ?content
                          :where [?e :block/string ?content]]
                        @conn)]
    (filter #(clojure.string/includes? % search-term) all-blocks)))

;; ✅ Efficient: Use external search index
(defn search-blocks-optimized [search-term]
  ;; Use a separate search index (Lucene, etc.)
  (search-index query search-term))
```

## 🧪 Hands-On Exercise

**Estimated Time: 60 minutes**

1. **Schema Design**: Design a complete schema for a knowledge management system
2. **Entity Relationships**: Model complex relationships between blocks, pages, and references
3. **Query Optimization**: Write efficient queries for common operations
4. **Migration Planning**: Plan schema changes and migration strategies
5. **Performance Testing**: Compare query performance with different schema designs

---

**Ready to explore ClojureScript architecture?** Continue to [Chapter 4: Application Architecture](04-app-architecture.md)