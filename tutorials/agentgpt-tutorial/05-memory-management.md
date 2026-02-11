---
layout: default
title: "Chapter 5: Memory & Context Management"
parent: "AgentGPT Tutorial"
nav_order: 5
---

# Chapter 5: Memory & Context Management

This chapter explores how AgentGPT agents manage memory, maintain context, and learn from past interactions to improve future performance.

## 🧠 Memory System Architecture

### Memory Types

```typescript
// Different types of agent memory
enum MemoryType {
  EPISODIC = 'episodic',     // Personal experiences and events
  SEMANTIC = 'semantic',     // Factual knowledge and concepts
  PROCEDURAL = 'procedural',  // Skills and procedures
  WORKING = 'working'        // Current context and temporary data
}

interface Memory {
  id: string
  type: MemoryType
  content: any
  timestamp: Date
  importance: number
  accessCount: number
  lastAccessed: Date
  tags: string[]
}
```

### Memory Manager

```typescript
// Central memory management system
class MemoryManager {
  private memories = new Map<string, Memory>()
  private maxMemories = 10000
  private consolidationInterval = 3600000 // 1 hour

  constructor() {
    setInterval(() => this.consolidateMemories(), this.consolidationInterval)
  }

  async store(memory: Omit<Memory, 'id' | 'timestamp' | 'accessCount' | 'lastAccessed'>): Promise<string> {
    const id = this.generateId()
    const fullMemory: Memory = {
      ...memory,
      id,
      timestamp: new Date(),
      accessCount: 0,
      lastAccessed: new Date()
    }

    this.memories.set(id, fullMemory)
    await this.persistMemory(fullMemory)

    // Trigger consolidation if needed
    if (this.memories.size > this.maxMemories * 0.9) {
      await this.consolidateMemories()
    }

    return id
  }

  async retrieve(query: MemoryQuery): Promise<Memory[]> {
    const candidates = Array.from(this.memories.values())

    // Filter by criteria
    let results = candidates.filter(memory => this.matchesQuery(memory, query))

    // Sort by relevance
    results.sort((a, b) => this.calculateRelevance(b, query) - this.calculateRelevance(a, query))

    // Update access statistics
    results.forEach(memory => this.updateAccessStats(memory))

    return results.slice(0, query.limit || 10)
  }
}
```

## 💭 Context Management

### Conversation Context

```typescript
// Manage conversation context
class ContextManager {
  private context: ConversationContext
  private maxContextLength = 10
  private contextWindow = 5

  constructor() {
    this.context = {
      messages: [],
      currentTopic: null,
      userPreferences: {},
      sessionStart: new Date(),
      metadata: {}
    }
  }

  addMessage(message: ChatMessage) {
    this.context.messages.push(message)

    // Maintain context window
    if (this.context.messages.length > this.maxContextLength) {
      this.context.messages.shift()
    }

    // Update topic analysis
    this.updateTopicAnalysis(message)

    // Store in long-term memory
    this.storeContextSnapshot()
  }

  getRelevantContext(query?: string): ConversationContext {
    if (!query) {
      return this.getRecentContext()
    }

    // Find contextually relevant messages
    const relevantMessages = this.findRelevantMessages(query)
    return {
      ...this.context,
      messages: relevantMessages
    }
  }

  private findRelevantMessages(query: string): ChatMessage[] {
    const queryTerms = query.toLowerCase().split(' ')

    return this.context.messages
      .filter(message =>
        queryTerms.some(term =>
          message.content.toLowerCase().includes(term)
        )
      )
      .slice(-this.contextWindow)
  }
}
```

### Working Memory

```typescript
// Short-term working memory
class WorkingMemory {
  private memory = new Map<string, any>()
  private ttl = new Map<string, number>()
  private cleanupInterval = 60000 // 1 minute

  constructor() {
    setInterval(() => this.cleanup(), this.cleanupInterval)
  }

  set(key: string, value: any, ttlMs: number = 300000) { // 5 minutes default
    this.memory.set(key, value)
    this.ttl.set(key, Date.now() + ttlMs)
  }

  get(key: string): any {
    this.updateAccessTime(key)
    return this.memory.get(key)
  }

  has(key: string): boolean {
    return this.memory.has(key) && !this.isExpired(key)
  }

  private updateAccessTime(key: string) {
    if (this.ttl.has(key)) {
      const currentTtl = this.ttl.get(key)!
      const now = Date.now()
      const remaining = currentTtl - now

      // Refresh TTL on access (sliding expiration)
      this.ttl.set(key, now + Math.min(remaining, 300000))
    }
  }

  private isExpired(key: string): boolean {
    const expiry = this.ttl.get(key)
    return expiry ? Date.now() > expiry : false
  }

  private cleanup() {
    const now = Date.now()
    const expiredKeys: string[] = []

    for (const [key, expiry] of this.ttl.entries()) {
      if (now > expiry) {
        expiredKeys.push(key)
      }
    }

    expiredKeys.forEach(key => {
      this.memory.delete(key)
      this.ttl.delete(key)
    })
  }
}
```

## 🧠 Long-term Memory

### Semantic Memory

```typescript
// Factual knowledge storage
class SemanticMemory {
  private knowledge = new Map<string, KnowledgeItem>()

  async learn(fact: string, category: string, confidence: number = 1.0) {
    const key = this.generateKey(fact)
    const item: KnowledgeItem = {
      fact,
      category,
      confidence,
      learnedAt: new Date(),
      accessCount: 0,
      relatedFacts: await this.findRelatedFacts(fact)
    }

    this.knowledge.set(key, item)
    await this.updateKnowledgeGraph(item)
  }

  async recall(query: string, category?: string): Promise<KnowledgeItem[]> {
    const candidates = Array.from(this.knowledge.values())

    let results = candidates.filter(item =>
      item.fact.toLowerCase().includes(query.toLowerCase())
    )

    if (category) {
      results = results.filter(item => item.category === category)
    }

    // Update access statistics
    results.forEach(item => {
      item.accessCount++
      item.lastAccessed = new Date()
    })

    return results.sort((a, b) => b.confidence - a.confidence)
  }

  private async findRelatedFacts(fact: string): Promise<string[]> {
    // Find semantically related facts
    const related = []
    const factWords = fact.toLowerCase().split(' ')

    for (const [key, item] of this.knowledge.entries()) {
      const overlap = factWords.filter(word =>
        item.fact.toLowerCase().includes(word)
      ).length

      if (overlap > 0) {
        related.push(key)
      }
    }

    return related
  }
}
```

### Episodic Memory

```typescript
// Experience-based memory
class EpisodicMemory {
  private episodes: Episode[] = []
  private maxEpisodes = 1000

  async storeEpisode(episode: Omit<Episode, 'id' | 'timestamp'>) {
    const fullEpisode: Episode = {
      ...episode,
      id: this.generateId(),
      timestamp: new Date()
    }

    this.episodes.push(fullEpisode)

    // Maintain memory limit
    if (this.episodes.length > this.maxEpisodes) {
      this.consolidateEpisodes()
    }

    await this.persistEpisode(fullEpisode)
  }

  async retrieveSimilar(currentSituation: any): Promise<Episode[]> {
    const similarities = this.episodes.map(episode => ({
      episode,
      similarity: this.calculateSimilarity(episode.situation, currentSituation)
    }))

    return similarities
      .filter(s => s.similarity > 0.3)
      .sort((a, b) => b.similarity - a.similarity)
      .map(s => s.episode)
      .slice(0, 5)
  }

  private calculateSimilarity(situation1: any, situation2: any): number {
    // Calculate similarity between situations
    const keys1 = Object.keys(situation1)
    const keys2 = Object.keys(situation2)

    const commonKeys = keys1.filter(key => keys2.includes(key))
    const totalKeys = new Set([...keys1, ...keys2]).size

    let similarity = commonKeys.length / totalKeys

    // Factor in value similarities
    for (const key of commonKeys) {
      if (situation1[key] === situation2[key]) {
        similarity += 0.1
      }
    }

    return Math.min(similarity, 1.0)
  }

  private consolidateEpisodes() {
    // Consolidate similar episodes
    const consolidated = new Map<string, Episode[]>()

    this.episodes.forEach(episode => {
      const key = this.generateEpisodeKey(episode)
      if (!consolidated.has(key)) {
        consolidated.set(key, [])
      }
      consolidated.get(key)!.push(episode)
    })

    // Keep most representative episode from each group
    this.episodes = Array.from(consolidated.values())
      .map(group => this.selectRepresentativeEpisode(group))
  }
}
```

## 🎯 Memory Consolidation

### Memory Strengthening

```typescript
// Strengthen important memories
class MemoryConsolidator {
  async consolidate(memory: Memory): Promise<Memory> {
    const strengthened = { ...memory }

    // Increase importance based on access patterns
    strengthened.importance = this.calculateImportance(memory)

    // Compress less important details
    if (memory.type === MemoryType.EPISODIC && memory.importance < 0.5) {
      strengthened.content = this.compressContent(memory.content)
    }

    // Update consolidation timestamp
    strengthened.consolidatedAt = new Date()

    return strengthened
  }

  private calculateImportance(memory: Memory): number {
    const baseImportance = memory.importance
    const accessBonus = Math.min(memory.accessCount * 0.1, 1.0)
    const recencyBonus = this.calculateRecencyBonus(memory.lastAccessed)

    return Math.min(baseImportance + accessBonus + recencyBonus, 1.0)
  }

  private calculateRecencyBonus(lastAccessed: Date): number {
    const daysSinceAccess = (Date.now() - lastAccessed.getTime()) / (1000 * 60 * 60 * 24)
    return Math.max(0, 1 - daysSinceAccess / 30) * 0.2 // Bonus decreases over 30 days
  }

  private compressContent(content: any): any {
    // Compress episodic content while preserving key information
    if (typeof content === 'object' && content.details) {
      return {
        summary: content.summary || this.generateSummary(content),
        keyPoints: content.keyPoints || this.extractKeyPoints(content),
        timestamp: content.timestamp
      }
    }
    return content
  }
}
```

## 🔍 Memory Retrieval

### Intelligent Retrieval

```typescript
// Intelligent memory retrieval
class MemoryRetriever {
  async retrieve(query: MemoryQuery): Promise<Memory[]> {
    const candidates = await this.findCandidates(query)

    // Rank by relevance
    const ranked = await this.rankMemories(candidates, query)

    // Apply context filtering
    const contextual = await this.applyContextFiltering(ranked, query.context)

    // Return top results
    return contextual.slice(0, query.limit || 10)
  }

  private async findCandidates(query: MemoryQuery): Promise<Memory[]> {
    const candidates: Memory[] = []

    // Search different memory types
    if (query.includeEpisodic) {
      candidates.push(...await this.searchEpisodicMemory(query))
    }

    if (query.includeSemantic) {
      candidates.push(...await this.searchSemanticMemory(query))
    }

    if (query.includeProcedural) {
      candidates.push(...await this.searchProceduralMemory(query))
    }

    return candidates
  }

  private async rankMemories(memories: Memory[], query: MemoryQuery): Promise<Memory[]> {
    const scored = await Promise.all(
      memories.map(async memory => ({
        memory,
        score: await this.calculateRelevanceScore(memory, query)
      }))
    )

    return scored
      .sort((a, b) => b.score - a.score)
      .map(item => item.memory)
  }

  private async calculateRelevanceScore(memory: Memory, query: MemoryQuery): Promise<number> {
    let score = 0

    // Content similarity
    score += this.calculateContentSimilarity(memory.content, query.content) * 0.4

    // Importance weight
    score += memory.importance * 0.2

    // Recency bonus
    score += this.calculateRecencyScore(memory.lastAccessed) * 0.2

    // Access frequency bonus
    score += Math.min(memory.accessCount / 10, 1) * 0.2

    return score
  }
}
```

## 📊 Memory Analytics

### Usage Statistics

```typescript
// Track memory system performance
class MemoryAnalytics {
  private stats = {
    totalMemories: 0,
    retrievals: 0,
    averageRetrievalTime: 0,
    hitRate: 0,
    memoryUsage: 0
  }

  recordRetrieval(query: MemoryQuery, results: Memory[], duration: number) {
    this.stats.retrievals++
    this.stats.averageRetrievalTime =
      (this.stats.averageRetrievalTime + duration) / 2

    if (results.length > 0) {
      this.stats.hitRate = (this.stats.hitRate + 1) / 2
    } else {
      this.stats.hitRate = this.stats.hitRate / 2
    }
  }

  getStats() {
    return { ...this.stats }
  }

  generateReport(): MemoryReport {
    return {
      summary: {
        totalMemories: this.stats.totalMemories,
        retrievals: this.stats.retrievals,
        hitRate: this.stats.hitRate,
        averageRetrievalTime: this.stats.averageRetrievalTime
      },
      recommendations: this.generateRecommendations(),
      trends: this.analyzeTrends()
    }
  }

  private generateRecommendations(): string[] {
    const recommendations = []

    if (this.stats.hitRate < 0.5) {
      recommendations.push('Consider improving memory indexing')
    }

    if (this.stats.averageRetrievalTime > 1000) {
      recommendations.push('Optimize memory retrieval algorithms')
    }

    return recommendations
  }
}
```

## 📝 Chapter Summary

- ✅ Built comprehensive memory system architecture
- ✅ Implemented conversation context management
- ✅ Created working and long-term memory systems
- ✅ Developed memory consolidation processes
- ✅ Built intelligent memory retrieval
- ✅ Set up memory analytics and monitoring

**Key Takeaways:**
- Multiple memory types serve different purposes
- Context management is crucial for coherent conversations
- Memory consolidation prevents information overload
- Intelligent retrieval improves agent performance
- Analytics help optimize memory systems
- Regular maintenance ensures memory system health
