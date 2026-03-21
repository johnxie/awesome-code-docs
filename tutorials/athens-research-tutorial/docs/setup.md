# Athens Research Development Environment Setup

## Prerequisites

### Required Software
- **Node.js 16+** with yarn package manager
- **Java 8+** (required for ClojureScript compilation)
- **Git** for version control
- **Chrome/Firefox** with developer tools

### Recommended Tools
- **VS Code** with Calva extension (ClojureScript support)
- **Cursive** (IntelliJ plugin) or **Emacs** with CIDER
- **Chrome DevTools** for debugging
- **Datascript DevTools** browser extension

## Installation Options

### Option 1: Local Development (Recommended)

```bash
# Clone the Athens Research repository
git clone https://github.com/athensresearch/athens.git
cd athens

# Install dependencies
yarn install

# Start development server
yarn dev

# In another terminal, start the electron app
yarn electron:dev
```

### Option 2: Web-Only Development

```bash
# Clone the repository
git clone https://github.com/athensresearch/athens.git
cd athens

# Install dependencies
yarn install

# Start web development server only
yarn dev:web

# Access at http://localhost:3000
```

## Project Structure Overview

```
athens/
├── src/
│   ├── cljs/athens/         # Main ClojureScript source
│   │   ├── core.cljs        # Application entry point
│   │   ├── db/              # Datascript database layer
│   │   │   ├── schema.cljs  # Database schema definition
│   │   │   └── utils.cljs   # Database utility functions
│   │   ├── views/           # Reagent UI components
│   │   │   ├── blocks/      # Block editor components
│   │   │   ├── pages/       # Page view components
│   │   │   └── graph/       # Graph visualization
│   │   ├── events/          # Re-frame event handlers
│   │   ├── effects/         # Re-frame effect handlers
│   │   └── subs/            # Re-frame subscriptions
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript interop
├── resources/public/        # Static assets
├── test/                    # Test files
└── shadow-cljs.edn         # ClojureScript build configuration
```

## ClojureScript Development Setup

### VS Code with Calva

1. Install the Calva extension
2. Open the Athens project in VS Code
3. Connect to REPL: `Ctrl+Shift+P` → "Calva: Connect to a Running REPL"
4. Select `shadow-cljs` and `:app` build

```json
// .vscode/settings.json
{
  "calva.replConnectSequences": [
    {
      "name": "Athens Development",
      "projectType": "shadow-cljs",
      "builds": [":app"]
    }
  ]
}
```

### REPL-Driven Development

```clojure
;; In your REPL, you can interact with the running application
(require '[athens.db :as db])
(require '[athens.views.blocks :as blocks])

;; Query the current database
(db/q '[:find ?e ?title
        :where [?e :page/title ?title]]
      @db/dsdb)

;; Create a new block
(db/transact! [{:block/uid (db/gen-block-uid)
                :block/string "Hello from the REPL!"
                :block/page [:page/title "Daily Notes"]}])
```

## Database Development

### Datascript Schema

Athens uses Datascript, an in-memory database. Understanding the schema is crucial:

```clojure
;; Core schema in src/cljs/athens/db/schema.cljs
{:page/title       {:db/unique :db.unique/identity}
 :page/uid         {:db/unique :db.unique/identity}
 :block/uid        {:db/unique :db.unique/identity}
 :block/string     {}
 :block/children   {:db/valueType :db.type/ref
                    :db/cardinality :db.cardinality/many}
 :block/refs       {:db/valueType :db.type/ref
                    :db/cardinality :db.cardinality/many}}
```

### Database Queries

```clojure
;; Find all pages
(db/q '[:find ?title
        :where [_ :page/title ?title]]
      @db/dsdb)

;; Find blocks containing specific text
(db/q '[:find ?uid ?string
        :in $ ?search-term
        :where 
        [?e :block/uid ?uid]
        [?e :block/string ?string]
        [(clojure.string/includes? ?string ?search-term)]]
      @db/dsdb
      "ClojureScript")

;; Find backlinks to a page
(db/q '[:find ?source-uid ?source-string
        :in $ ?target-title
        :where
        [?target :page/title ?target-title]
        [?source :block/refs ?target]
        [?source :block/uid ?source-uid]
        [?source :block/string ?source-string]]
      @db/dsdb
      "My Page Title")
```

## Component Development

### Creating a New Block Type

```clojure
;; In src/cljs/athens/views/blocks/
(ns athens.views.blocks.my-block
  (:require [reagent.core :as r]
            [athens.db :as db]
            [athens.events :as events]))

(defn my-custom-block
  "A custom block type with special functionality"
  [block]
  (let [uid     (:block/uid block)
        string  (:block/string block)
        editing (r/atom false)]
    (fn [block]
      [:div.block-container
       {:data-uid uid}
       (if @editing
         [:textarea
          {:value string
           :on-blur #(do (reset! editing false)
                        (events/update-block uid (-> % .-target .-value)))
           :auto-focus true}]
         [:div.block-content
          {:on-click #(reset! editing true)}
          string])])))
```

### Adding Event Handlers

```clojure
;; In src/cljs/athens/events/
(rf/reg-event-fx
  :block/create-custom
  (fn [{:keys [db]} [_ parent-uid block-data]]
    (let [new-uid (db/gen-block-uid)
          new-block (merge {:block/uid new-uid
                           :block/string ""
                           :block/open true}
                          block-data)]
      {:db (db/transact! db [new-block
                             {:db/id [:block/uid parent-uid]
                              :block/children new-uid}])
       :dispatch [:navigate/to-block new-uid]})))
```

## Testing Setup

### Running Tests

```bash
# Run all tests
yarn test

# Run specific namespace tests
yarn test athens.db.utils-test

# Run tests with watch mode
yarn test:watch
```

### Writing Tests

```clojure
;; In test/athens/db/utils_test.cljs
(ns athens.db.utils-test
  (:require [cljs.test :refer-macros [deftest testing is]]
            [athens.db.utils :as utils]))

(deftest block-creation-test
  (testing "Block UID generation"
    (let [uid (utils/gen-block-uid)]
      (is (string? uid))
      (is (= 9 (count uid)))
      (is (utils/valid-uid? uid)))))

(deftest bi-directional-links-test
  (testing "Link parsing and creation"
    (let [text "Check out [[My Page]] and [[Another Page]]"
          links (utils/parse-page-links text)]
      (is (= 2 (count links)))
      (is (contains? (set links) "My Page"))
      (is (contains? (set links) "Another Page")))))
```

## Development Workflow

### Making Changes

**Frontend Changes:**
```bash
# ClojureScript hot-reloading is automatic
# Just save your .cljs files and see changes immediately

# For CSS changes
yarn css:watch
```

**Database Schema Changes:**
```bash
# 1. Update schema in src/cljs/athens/db/schema.cljs
# 2. Create migration in src/cljs/athens/db/migrations.cljs
# 3. Test with sample data
```

### Debugging Tips

**Using Browser DevTools:**
```javascript
// In browser console, access the Athens namespace
athens.core.hello()

// Inspect current database state
athens.db.dsdb.deref()

// Query database from console
athens.db.q("[[:find ?e :where [?e :page/title]]]", athens.db.dsdb.deref())
```

**REPL Debugging:**
```clojure
;; Set breakpoints with tap>
(tap> {:debugging-data some-variable})

;; Use prn for simple debugging
(prn "Current block:" block)

;; Use cljs.pprint for complex data structures
(cljs.pprint/pprint complex-data)
```

## Common Development Tasks

### Adding a New Page Type

1. Define schema in `schema.cljs`
2. Create view component in `views/pages/`
3. Add event handlers in `events/`
4. Update routing in `router.cljs`
5. Add tests

### Implementing a New Query

1. Write query in `db/queries.cljs`
2. Create subscription in `subs.cljs`
3. Use in component with `@(rf/subscribe [:query-name])`
4. Test with sample data

### Building Custom Block Types

1. Create component in `views/blocks/`
2. Register in block registry
3. Add parsing rules if needed
4. Implement serialization
5. Add tests and examples

## Troubleshooting

### Common Issues

**ClojureScript Compilation Errors:**
```bash
# Clear compiled files
rm -rf .shadow-cljs/
yarn clean

# Restart development server
yarn dev
```

**REPL Connection Issues:**
```bash
# Kill existing processes
pkill -f shadow-cljs
yarn dev
```

**Database State Issues:**
```clojure
;; Reset database to initial state
(athens.db/reset-conn!)

;; Load sample data
(athens.db/load-sample-data!)
```

## Next Steps

Once your environment is set up:

1. **Explore the Database** - Query existing data and understand the schema
2. **Create Your First Block** - Use the REPL to add content
3. **Build a Simple Component** - Create a basic UI element
4. **Study the Architecture** - Application Architecture (planned)

## Getting Help

- **Setup Issues**: [Open an issue](https://github.com/johnxie/awesome-code-docs/issues) with `[athens-setup]` tag
- **Athens Community**: [Official Discord](https://discord.gg/GCJaV3V)
- **ClojureScript Questions**: [ClojureVerse Forum](https://clojureverse.org/)

---

**✅ Environment ready? Continue to [System Overview](../01-system-overview.md)**
