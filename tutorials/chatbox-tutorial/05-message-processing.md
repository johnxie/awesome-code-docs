---
layout: default
title: "Chapter 5: Message Processing Pipeline"
parent: "Chatbox Tutorial"
nav_order: 5
---

# Chapter 5: Message Processing Pipeline

This chapter covers the message processing pipeline, including text processing, formatting, and content enhancement.

## 🔄 Message Processing Architecture

### Processing Pipeline

```typescript
// Message processing pipeline
class MessageProcessingPipeline {
  private processors: MessageProcessor[] = []

  addProcessor(processor: MessageProcessor) {
    this.processors.push(processor)
  }

  async process(message: IncomingMessage): Promise<ProcessedMessage> {
    let processedMessage = { ...message }

    for (const processor of this.processors) {
      try {
        processedMessage = await processor.process(processedMessage)
      } catch (error) {
        console.error(`Processor ${processor.name} failed:`, error)
        // Continue with other processors
      }
    }

    return processedMessage
  }

  async processBatch(messages: IncomingMessage[]): Promise<ProcessedMessage[]> {
    return Promise.all(messages.map(message => this.process(message)))
  }
}
```

### Message Processor Interface

```typescript
// Message processor interface
interface MessageProcessor {
  name: string
  process(message: ProcessedMessage): Promise<ProcessedMessage>
}

interface ProcessedMessage {
  id: string
  content: string
  timestamp: Date
  metadata: {
    originalLength: number
    processedLength: number
    processingTime: number
    processors: string[]
  }
  formatting?: MessageFormatting
  attachments?: Attachment[]
  mentions?: Mention[]
  links?: Link[]
}
```

## 📝 Text Processing

### Content Sanitization

```typescript
// Message content sanitization
class ContentSanitizer implements MessageProcessor {
  name = 'contentSanitizer'

  async process(message: ProcessedMessage): Promise<ProcessedMessage> {
    const sanitized = { ...message }

    // Remove potentially harmful content
    sanitized.content = this.sanitizeText(message.content)

    // Update metadata
    sanitized.metadata.processors.push(this.name)

    return sanitized
  }

  private sanitizeText(text: string): string {
    // Remove script tags
    text = text.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')

    // Remove potentially dangerous URLs
    text = text.replace(/javascript:/gi, '')
    text = text.replace(/data:text\/html/gi, '')

    // Remove excessive whitespace
    text = text.replace(/\s+/g, ' ').trim()

    return text
  }
}
```

### Text Normalization

```typescript
// Text normalization processor
class TextNormalizer implements MessageProcessor {
  name = 'textNormalizer'

  async process(message: ProcessedMessage): Promise<ProcessedMessage> {
    const normalized = { ...message }

    // Normalize unicode characters
    normalized.content = this.normalizeUnicode(message.content)

    // Normalize whitespace
    normalized.content = this.normalizeWhitespace(message.content)

    // Normalize quotes and apostrophes
    normalized.content = this.normalizeQuotes(message.content)

    normalized.metadata.processors.push(this.name)

    return normalized
  }

  private normalizeUnicode(text: string): string {
    return text
      .normalize('NFKC') // Compatibility decomposition followed by canonical composition
      .replace(/[\u2018\u2019]/g, "'") // Smart quotes to regular apostrophes
      .replace(/[\u201C\u201D]/g, '"') // Smart quotes to regular quotes
  }

  private normalizeWhitespace(text: string): string {
    return text
      .replace(/[\u00A0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]/g, ' ') // Various unicode spaces
      .replace(/\s+/g, ' ') // Multiple spaces to single
      .trim()
  }

  private normalizeQuotes(text: string): string {
    return text
      .replace(/["""]/g, '"') // Various quote marks to standard quotes
      .replace(/[''']/g, "'") // Various apostrophes to standard apostrophe
  }
}
```

## 🎨 Message Formatting

### Rich Text Formatting

```typescript
// Message formatting processor
class MessageFormatter implements MessageProcessor {
  name = 'messageFormatter'

  async process(message: ProcessedMessage): Promise<ProcessedMessage> {
    const formatted = { ...message }

    // Parse markdown
    formatted.content = this.parseMarkdown(message.content)

    // Apply syntax highlighting
    formatted.content = this.applySyntaxHighlighting(message.content)

    // Extract formatting metadata
    formatted.formatting = this.extractFormatting(message.content)

    formatted.metadata.processors.push(this.name)

    return formatted
  }

  private parseMarkdown(text: string): string {
    // Basic markdown parsing
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
      .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
      .replace(/`(.*?)`/g, '<code>$1</code>') // Inline code
      .replace(/\n/g, '<br>') // Line breaks
  }

  private applySyntaxHighlighting(text: string): string {
    // Basic syntax highlighting for code blocks
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g

    return text.replace(codeBlockRegex, (match, language, code) => {
      const highlighted = this.highlightCode(code, language)
      return `<pre><code class="language-${language}">${highlighted}</code></pre>`
    })
  }

  private highlightCode(code: string, language: string): string {
    // Basic syntax highlighting (simplified)
    switch (language) {
      case 'javascript':
      case 'typescript':
        return code
          .replace(/\b(function|const|let|var|if|else|for|while)\b/g, '<span class="keyword">$1</span>')
          .replace(/(\/\/.*$)/gm, '<span class="comment">$1</span>')
          .replace(/(".*?"|'.*?')/g, '<span class="string">$1</span>')
      default:
        return code
    }
  }

  private extractFormatting(text: string): MessageFormatting {
    return {
      hasBold: /\*\*.*?\*\*/.test(text),
      hasItalic: /\*.*?\*/.test(text),
      hasCode: /`.*?`/.test(text),
      hasLinks: /https?:\/\/[^\s]+/.test(text),
      codeBlocks: (text.match(/```[\s\S]*?```/g) || []).length
    }
  }
}
```

## 🔗 Link Processing

### Link Detection and Enhancement

```typescript
// Link processing
class LinkProcessor implements MessageProcessor {
  name = 'linkProcessor'

  async process(message: ProcessedMessage): Promise<ProcessedMessage> {
    const processed = { ...message }

    // Extract links
    processed.links = this.extractLinks(message.content)

    // Enhance links with metadata
    processed.links = await Promise.all(
      processed.links.map(link => this.enhanceLink(link))
    )

    // Convert plain URLs to clickable links
    processed.content = this.convertUrlsToLinks(message.content)

    processed.metadata.processors.push(this.name)

    return processed
  }

  private extractLinks(text: string): Link[] {
    const urlRegex = /https?:\/\/[^\s]+/g
    const matches = text.match(urlRegex) || []

    return matches.map(url => ({
      url,
      text: url,
      title: '',
      description: '',
      image: '',
      type: this.detectLinkType(url)
    }))
  }

  private async enhanceLink(link: Link): Promise<Link> {
    try {
      // Fetch link metadata (simplified)
      const metadata = await this.fetchLinkMetadata(link.url)
      return { ...link, ...metadata }
    } catch (error) {
      console.warn(`Failed to fetch metadata for ${link.url}:`, error)
      return link
    }
  }

  private detectLinkType(url: string): LinkType {
    if (/\.(jpg|jpeg|png|gif|webp)$/i.test(url)) return 'image'
    if (/\.(mp4|avi|mov|webm)$/i.test(url)) return 'video'
    if (/youtube\.com|youtu\.be|vimeo\.com/i.test(url)) return 'video'
    if (/twitter\.com|x\.com/i.test(url)) return 'social'
    return 'website'
  }

  private convertUrlsToLinks(text: string): string {
    return text.replace(
      /(https?:\/\/[^\s]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    )
  }
}
```

## 👥 Mention Processing

### User and Channel Mentions

```typescript
// Mention processing
class MentionProcessor implements MessageProcessor {
  name = 'mentionProcessor'

  async process(message: ProcessedMessage): Promise<ProcessedMessage> {
    const processed = { ...message }

    // Extract mentions
    processed.mentions = this.extractMentions(message.content)

    // Validate mentions
    processed.mentions = await this.validateMentions(processed.mentions)

    // Highlight mentions in content
    processed.content = this.highlightMentions(message.content, processed.mentions)

    processed.metadata.processors.push(this.name)

    return processed
  }

  private extractMentions(text: string): Mention[] {
    const mentionRegex = /@(\w+)/g
    const matches = text.match(mentionRegex) || []

    return matches.map(match => ({
      username: match.slice(1),
      type: 'user' as const,
      position: text.indexOf(match),
      isValid: false
    }))
  }

  private async validateMentions(mentions: Mention[]): Promise<Mention[]> {
    // Validate against user database
    return Promise.all(
      mentions.map(async mention => ({
        ...mention,
        isValid: await this.userExists(mention.username)
      }))
    )
  }

  private highlightMentions(text: string, mentions: Mention[]): string {
    let highlighted = text

    mentions.forEach(mention => {
      if (mention.isValid) {
        const regex = new RegExp(`@${mention.username}`, 'g')
        highlighted = highlighted.replace(regex, `<span class="mention">@${mention.username}</span>`)
      }
    })

    return highlighted
  }
}
```

## 📎 Attachment Processing

### File and Media Processing

```typescript
// Attachment processing
class AttachmentProcessor implements MessageProcessor {
  name = 'attachmentProcessor'

  async process(message: ProcessedMessage): Promise<ProcessedMessage> {
    const processed = { ...message }

    // Process file attachments
    if (message.attachments) {
      processed.attachments = await Promise.all(
        message.attachments.map(attachment => this.processAttachment(attachment))
      )
    }

    processed.metadata.processors.push(this.name)

    return processed
  }

  private async processAttachment(attachment: Attachment): Promise<ProcessedAttachment> {
    const processed: ProcessedAttachment = {
      ...attachment,
      processed: true,
      metadata: {}
    }

    // Process based on file type
    switch (attachment.type) {
      case 'image':
        processed.metadata = await this.processImage(attachment)
        break
      case 'video':
        processed.metadata = await this.processVideo(attachment)
        break
      case 'document':
        processed.metadata = await this.processDocument(attachment)
        break
    }

    return processed
  }

  private async processImage(attachment: Attachment): Promise<ImageMetadata> {
    // Extract image metadata
    return {
      dimensions: await this.getImageDimensions(attachment.url),
      format: this.getImageFormat(attachment.filename),
      size: attachment.size,
      thumbnail: await this.generateThumbnail(attachment.url)
    }
  }

  private async processVideo(attachment: Attachment): Promise<VideoMetadata> {
    return {
      duration: await this.getVideoDuration(attachment.url),
      dimensions: await this.getVideoDimensions(attachment.url),
      format: this.getVideoFormat(attachment.filename),
      thumbnail: await this.generateVideoThumbnail(attachment.url)
    }
  }

  private async processDocument(attachment: Attachment): Promise<DocumentMetadata> {
    return {
      pages: await this.getDocumentPages(attachment.url),
      format: this.getDocumentFormat(attachment.filename),
      textContent: await this.extractTextContent(attachment.url)
    }
  }
}
```

## ⚡ Performance Optimization

### Processing Optimization

```typescript
// Optimized processing pipeline
class OptimizedProcessingPipeline extends MessageProcessingPipeline {
  private cache = new Map<string, ProcessedMessage>()
  private batchQueue: IncomingMessage[] = []
  private batchSize = 10
  private batchTimeout = 100 // ms

  async process(message: IncomingMessage): Promise<ProcessedMessage> {
    // Check cache first
    const cacheKey = this.generateCacheKey(message)
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)!
    }

    // Add to batch queue
    this.batchQueue.push(message)

    // Process batch if ready
    if (this.batchQueue.length >= this.batchSize) {
      return await this.processBatchAndReturn(message)
    }

    // Wait for batch timeout
    return new Promise((resolve) => {
      setTimeout(async () => {
        resolve(await this.processBatchAndReturn(message))
      }, this.batchTimeout)
    })
  }

  private async processBatchAndReturn(targetMessage: IncomingMessage): Promise<ProcessedMessage> {
    const batch = [...this.batchQueue]
    this.batchQueue = []

    const results = await this.processBatch(batch)
    const result = results.find(r => r.id === targetMessage.id)

    if (result) {
      // Cache result
      const cacheKey = this.generateCacheKey(targetMessage)
      this.cache.set(cacheKey, result)

      // Cleanup old cache entries
      this.cleanupCache()
    }

    return result!
  }

  private generateCacheKey(message: IncomingMessage): string {
    // Generate deterministic cache key
    return `${message.content.length}-${this.hashString(message.content)}`
  }

  private hashString(str: string): string {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i)
      hash = hash & hash
    }
    return hash.toString()
  }

  private cleanupCache() {
    if (this.cache.size > 1000) {
      // Remove oldest 20% of entries
      const entries = Array.from(this.cache.entries())
      const toRemove = Math.floor(entries.length * 0.2)

      entries
        .sort((a, b) => this.getCacheAge(a[1]) - this.getCacheAge(b[1]))
        .slice(0, toRemove)
        .forEach(([key]) => this.cache.delete(key))
    }
  }

  private getCacheAge(message: ProcessedMessage): number {
    return Date.now() - message.timestamp.getTime()
  }
}
```

## 📊 Processing Analytics

### Performance Monitoring

```typescript
// Processing performance analytics
class ProcessingAnalytics {
  private metrics = {
    totalProcessed: 0,
    averageProcessingTime: 0,
    processorUsage: new Map<string, number>(),
    errorRate: 0,
    cacheHitRate: 0
  }

  recordProcessing(messageId: string, processors: string[], duration: number, cached: boolean) {
    this.metrics.totalProcessed++
    this.metrics.averageProcessingTime =
      (this.metrics.averageProcessingTime + duration) / 2

    // Record processor usage
    processors.forEach(processor => {
      const usage = this.metrics.processorUsage.get(processor) || 0
      this.metrics.processorUsage.set(processor, usage + 1)
    })

    // Update cache hit rate
    if (cached) {
      this.metrics.cacheHitRate = (this.metrics.cacheHitRate + 1) / 2
    } else {
      this.metrics.cacheHitRate = this.metrics.cacheHitRate / 2
    }
  }

  recordError(processor: string, error: Error) {
    this.metrics.errorRate = (this.metrics.errorRate + 1) / this.metrics.totalProcessed
    console.error(`Processing error in ${processor}:`, error)
  }

  getMetrics() {
    return {
      ...this.metrics,
      topProcessors: Array.from(this.metrics.processorUsage.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
    }
  }
}
```

## 📝 Chapter Summary

- ✅ Built comprehensive message processing pipeline
- ✅ Implemented text sanitization and normalization
- ✅ Created rich text formatting system
- ✅ Added link detection and enhancement
- ✅ Built mention processing system
- ✅ Developed attachment processing
- ✅ Added performance optimization
- ✅ Created processing analytics

**Key Takeaways:**
- Processing pipeline enables rich message handling
- Multiple processors can be chained together
- Caching improves performance for repeated content
- Analytics help identify bottlenecks
- Error handling ensures pipeline reliability
- Modularity allows easy extension
