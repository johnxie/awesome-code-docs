---
layout: default
title: "Chapter 7: Next.js Applications"
parent: "Vercel AI Tutorial"
nav_order: 7
---

# Chapter 7: Next.js Applications

Welcome to full-stack AI development! This chapter brings everything together - we'll build complete Next.js applications that combine AI capabilities with databases, authentication, real-time features, and production deployment. Get ready to create production-ready AI applications!

## AI-Powered Blog Platform

Let's build a complete blog platform with AI content generation:

```tsx
// app/page.tsx
import { BlogDashboard } from '@/components/BlogDashboard'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            AI Blog Studio
          </h1>
          <p className="text-gray-600 mt-2">
            Create amazing content with AI assistance
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <BlogDashboard />
      </main>
    </div>
  )
}
```

```tsx
// components/BlogDashboard.tsx
'use client'

import { useState, useEffect } from 'react'
import { AIContentEditor } from './AIContentEditor'
import { BlogPost } from '@/types/blog'

export function BlogDashboard() {
  const [posts, setPosts] = useState<BlogPost[]>([])
  const [selectedPost, setSelectedPost] = useState<BlogPost | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchPosts()
  }, [])

  const fetchPosts = async () => {
    try {
      const response = await fetch('/api/posts')
      const data = await response.json()
      setPosts(data.posts)
    } catch (error) {
      console.error('Failed to fetch posts:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const createNewPost = () => {
    const newPost: BlogPost = {
      id: Date.now().toString(),
      title: 'New Post',
      content: '',
      status: 'draft',
      createdAt: new Date(),
      updatedAt: new Date(),
    }
    setPosts(prev => [newPost, ...prev])
    setSelectedPost(newPost)
  }

  const savePost = async (post: BlogPost) => {
    try {
      const response = await fetch('/api/posts', {
        method: post.id.startsWith('temp') ? 'POST' : 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(post),
      })

      if (response.ok) {
        await fetchPosts() // Refresh the list
      }
    } catch (error) {
      console.error('Failed to save post:', error)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      {/* Sidebar */}
      <div className="lg:col-span-1">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Posts</h2>
            <button
              onClick={createNewPost}
              className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
            >
              New
            </button>
          </div>

          <div className="space-y-2">
            {posts.map((post) => (
              <div
                key={post.id}
                onClick={() => setSelectedPost(post)}
                className={`p-3 rounded cursor-pointer transition-colors ${
                  selectedPost?.id === post.id
                    ? 'bg-blue-50 border-blue-200'
                    : 'hover:bg-gray-50'
                }`}
              >
                <h3 className="font-medium text-sm truncate">{post.title}</h3>
                <p className="text-xs text-gray-500 mt-1">
                  {post.status} • {post.updatedAt.toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Editor */}
      <div className="lg:col-span-3">
        {selectedPost ? (
          <AIContentEditor
            post={selectedPost}
            onSave={savePost}
          />
        ) : (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <div className="text-6xl mb-4">📝</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Select a post to edit
            </h3>
            <p className="text-gray-600">
              Choose a post from the sidebar or create a new one
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
```

```tsx
// components/AIContentEditor.tsx
'use client'

import { useState } from 'react'
import { BlogPost } from '@/types/blog'
import { generateText } from 'ai'
import { openai } from '@ai-sdk/openai'

interface AIContentEditorProps {
  post: BlogPost
  onSave: (post: BlogPost) => void
}

export function AIContentEditor({ post, onSave }: AIContentEditorProps) {
  const [title, setTitle] = useState(post.title)
  const [content, setContent] = useState(post.content)
  const [isGenerating, setIsGenerating] = useState(false)
  const [selectedText, setSelectedText] = useState('')

  const handleSave = () => {
    const updatedPost: BlogPost = {
      ...post,
      title,
      content,
      updatedAt: new Date(),
    }
    onSave(updatedPost)
  }

  const generateTitle = async () => {
    if (!content.trim()) return

    setIsGenerating(true)
    try {
      const { text } = await generateText({
        model: openai('gpt-4'),
        prompt: `Generate a compelling title for this blog post content: "${content.substring(0, 500)}..."`,
      })
      setTitle(text)
    } catch (error) {
      console.error('Title generation error:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const improveContent = async () => {
    if (!selectedText) return

    setIsGenerating(true)
    try {
      const { text } = await generateText({
        model: openai('gpt-4'),
        prompt: `Improve this text for a blog post: "${selectedText}"`,
      })
      replaceSelectedText(text)
    } catch (error) {
      console.error('Content improvement error:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const replaceSelectedText = (newText: string) => {
    const textarea = document.getElementById('content-editor') as HTMLTextAreaElement
    const start = textarea.selectionStart
    const end = textarea.selectionEnd

    const newContent = content.substring(0, start) + newText + content.substring(end)
    setContent(newContent)
  }

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Header */}
      <div className="border-b p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Post title..."
              className="text-2xl font-bold w-full border-none outline-none"
            />
          </div>
          <div className="flex items-center space-x-2 ml-4">
            <button
              onClick={generateTitle}
              disabled={isGenerating}
              className="px-3 py-1 bg-purple-500 text-white rounded text-sm hover:bg-purple-600 disabled:opacity-50"
            >
              Generate Title
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            >
              Save
            </button>
          </div>
        </div>
      </div>

      {/* Toolbar */}
      <div className="border-b px-6 py-3">
        <div className="flex items-center space-x-2">
          <button
            onClick={improveContent}
            disabled={!selectedText || isGenerating}
            className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600 disabled:opacity-50"
          >
            Improve Selected
          </button>
          <button className="px-3 py-1 bg-gray-500 text-white rounded text-sm hover:bg-gray-600">
            Add Image
          </button>
          <button className="px-3 py-1 bg-gray-500 text-white rounded text-sm hover:bg-gray-600">
            Format
          </button>
        </div>

        {selectedText && (
          <div className="mt-2 text-sm text-gray-600">
            Selected: "{selectedText.length > 50 ? selectedText.substring(0, 50) + '...' : selectedText}"
          </div>
        )}
      </div>

      {/* Editor */}
      <div className="p-6">
        <textarea
          id="content-editor"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onSelect={(e) => {
            const target = e.target as HTMLTextAreaElement
            const start = target.selectionStart
            const end = target.selectionEnd
            setSelectedText(content.substring(start, end))
          }}
          placeholder="Start writing your blog post..."
          className="w-full h-96 border-none outline-none resize-none text-gray-800 leading-relaxed"
        />

        {isGenerating && (
          <div className="mt-4 text-sm text-gray-600 flex items-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-2"></div>
            AI is working...
          </div>
        )}
      </div>
    </div>
  )
}
```

## API Routes for Blog Management

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { prisma } from '@/lib/prisma'

export async function GET() {
  try {
    const session = await getServerSession()
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const posts = await prisma.post.findMany({
      where: { authorId: session.user.id },
      orderBy: { updatedAt: 'desc' },
    })

    return NextResponse.json({ posts })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch posts' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession()
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { title, content, status = 'draft' } = await request.json()

    const post = await prisma.post.create({
      data: {
        title,
        content,
        status,
        authorId: session.user.id,
      },
    })

    return NextResponse.json({ post })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create post' },
      { status: 500 }
    )
  }
}
```

```typescript
// app/api/posts/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { prisma } from '@/lib/prisma'

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession()
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { title, content, status } = await request.json()

    const post = await prisma.post.update({
      where: {
        id: params.id,
        authorId: session.user.id, // Ensure user can only update their own posts
      },
      data: { title, content, status },
    })

    return NextResponse.json({ post })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to update post' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession()
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    await prisma.post.delete({
      where: {
        id: params.id,
        authorId: session.user.id,
      },
    })

    return NextResponse.json({ success: true })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to delete post' },
      { status: 500 }
    )
  }
}
```

## AI-Powered Customer Support System

Let's build a customer support system with AI triage and responses:

```tsx
// app/support/page.tsx
import { SupportDashboard } from '@/components/SupportDashboard'

export default function SupportPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            AI Support Center
          </h1>
          <p className="text-gray-600 mt-2">
            Intelligent customer support with AI assistance
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <SupportDashboard />
      </main>
    </div>
  )
}
```

```tsx
// components/SupportDashboard.tsx
'use client'

import { useState, useEffect } from 'react'
import { SupportTicket } from '@/types/support'
import { AITriagePanel } from './AITriagePanel'
import { TicketList } from './TicketList'
import { ChatInterface } from './ChatInterface'

export function SupportDashboard() {
  const [tickets, setTickets] = useState<SupportTicket[]>([])
  const [selectedTicket, setSelectedTicket] = useState<SupportTicket | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchTickets()
  }, [])

  const fetchTickets = async () => {
    try {
      const response = await fetch('/api/support/tickets')
      const data = await response.json()
      setTickets(data.tickets)
    } catch (error) {
      console.error('Failed to fetch tickets:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const updateTicket = async (ticketId: string, updates: Partial<SupportTicket>) => {
    try {
      const response = await fetch(`/api/support/tickets/${ticketId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      })

      if (response.ok) {
        await fetchTickets()
        if (selectedTicket?.id === ticketId) {
          setSelectedTicket(prev => prev ? { ...prev, ...updates } : null)
        }
      }
    } catch (error) {
      console.error('Failed to update ticket:', error)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      {/* Ticket List */}
      <div className="lg:col-span-1">
        <TicketList
          tickets={tickets}
          selectedTicket={selectedTicket}
          onSelectTicket={setSelectedTicket}
        />
      </div>

      {/* Main Content */}
      <div className="lg:col-span-2">
        {selectedTicket ? (
          <ChatInterface
            ticket={selectedTicket}
            onUpdateTicket={updateTicket}
          />
        ) : (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <div className="text-6xl mb-4">🎫</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Select a ticket
            </h3>
            <p className="text-gray-600">
              Choose a support ticket to start assisting
            </p>
          </div>
        )}
      </div>

      {/* AI Triage Panel */}
      <div className="lg:col-span-1">
        <AITriagePanel
          ticket={selectedTicket}
          onUpdateTicket={updateTicket}
        />
      </div>
    </div>
  )
}
```

```tsx
// components/AITriagePanel.tsx
'use client'

import { useState } from 'react'
import { SupportTicket } from '@/types/support'
import { generateObject } from 'ai'
import { openai } from '@ai-sdk/openai'
import { z } from 'zod'

interface AITriagePanelProps {
  ticket: SupportTicket | null
  onUpdateTicket: (ticketId: string, updates: Partial<SupportTicket>) => void
}

const triageSchema = z.object({
  priority: z.enum(['low', 'medium', 'high', 'urgent']),
  category: z.enum(['technical', 'billing', 'account', 'feature', 'bug', 'other']),
  sentiment: z.enum(['positive', 'neutral', 'negative', 'angry']),
  suggestedResponse: z.string(),
  tags: z.array(z.string()),
})

export function AITriagePanel({ ticket, onUpdateTicket }: AITriagePanelProps) {
  const [triage, setTriage] = useState<any>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const analyzeTicket = async () => {
    if (!ticket) return

    setIsAnalyzing(true)
    try {
      const { object } = await generateObject({
        model: openai('gpt-4'),
        schema: triageSchema,
        prompt: `Analyze this customer support ticket and provide triage information:

Title: ${ticket.title}
Description: ${ticket.description}
Customer: ${ticket.customerName}
Priority: ${ticket.priority}
Status: ${ticket.status}

Provide:
- Priority assessment (low, medium, high, urgent)
- Category classification
- Customer sentiment
- Suggested response
- Relevant tags`,
      })

      setTriage(object)
    } catch (error) {
      console.error('Triage analysis error:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const applyTriage = () => {
    if (!ticket || !triage) return

    onUpdateTicket(ticket.id, {
      priority: triage.priority,
      category: triage.category,
      tags: triage.tags,
    })
  }

  if (!ticket) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">AI Triage</h3>
        <p className="text-gray-600">Select a ticket to analyze</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">AI Triage</h3>
        <button
          onClick={analyzeTicket}
          disabled={isAnalyzing}
          className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600 disabled:opacity-50"
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      {triage && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Priority</label>
            <span className={`px-2 py-1 rounded text-sm ${
              triage.priority === 'urgent' ? 'bg-red-100 text-red-800' :
              triage.priority === 'high' ? 'bg-orange-100 text-orange-800' :
              triage.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
              'bg-green-100 text-green-800'
            }`}>
              {triage.priority}
            </span>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Category</label>
            <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
              {triage.category}
            </span>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Sentiment</label>
            <span className={`px-2 py-1 rounded text-sm ${
              triage.sentiment === 'angry' ? 'bg-red-100 text-red-800' :
              triage.sentiment === 'negative' ? 'bg-orange-100 text-orange-800' :
              triage.sentiment === 'neutral' ? 'bg-gray-100 text-gray-800' :
              'bg-green-100 text-green-800'
            }`}>
              {triage.sentiment}
            </span>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Suggested Response</label>
            <p className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
              {triage.suggestedResponse}
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Tags</label>
            <div className="flex flex-wrap gap-1">
              {triage.tags.map((tag: string, index: number) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>

          <button
            onClick={applyTriage}
            className="w-full px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Apply Triage
          </button>
        </div>
      )}
    </div>
  )
}
```

## Real-time AI Collaboration System

Let's build a collaborative AI writing system:

```tsx
// app/collaborate/page.tsx
import { CollaborationStudio } from '@/components/CollaborationStudio'

export default function CollaboratePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <CollaborationStudio />
    </div>
  )
}
```

```tsx
// components/CollaborationStudio.tsx
'use client'

import { useState, useEffect, useRef } from 'react'
import { io, Socket } from 'socket.io-client'
import { AIWritingAssistant } from './AIWritingAssistant'
import { UserPresence } from './UserPresence'
import { DocumentEditor } from './DocumentEditor'

interface User {
  id: string
  name: string
  avatar?: string
  cursor?: { line: number; column: number }
}

export function CollaborationStudio() {
  const [document, setDocument] = useState('')
  const [users, setUsers] = useState<User[]>([])
  const [currentUser, setCurrentUser] = useState<User | null>(null)
  const socketRef = useRef<Socket | null>(null)

  useEffect(() => {
    // Initialize Socket.IO connection
    socketRef.current = io('/api/socket')

    socketRef.current.on('document-update', (newDocument: string) => {
      setDocument(newDocument)
    })

    socketRef.current.on('users-update', (updatedUsers: User[]) => {
      setUsers(updatedUsers)
    })

    socketRef.current.on('user-joined', (user: User) => {
      setUsers(prev => [...prev, user])
    })

    socketRef.current.on('user-left', (userId: string) => {
      setUsers(prev => prev.filter(u => u.id !== userId))
    })

    // Simulate current user
    const user: User = {
      id: Date.now().toString(),
      name: 'You',
      avatar: '👤',
    }
    setCurrentUser(user)

    return () => {
      socketRef.current?.disconnect()
    }
  }, [])

  const handleDocumentChange = (newDocument: string) => {
    setDocument(newDocument)
    socketRef.current?.emit('document-change', newDocument)
  }

  const handleCursorMove = (line: number, column: number) => {
    if (currentUser) {
      const updatedUser = { ...currentUser, cursor: { line, column } }
      setCurrentUser(updatedUser)
      socketRef.current?.emit('cursor-move', { line, column })
    }
  }

  return (
    <div className="h-screen flex">
      {/* Main Editor */}
      <div className="flex-1 flex flex-col">
        <div className="bg-white border-b p-4">
          <h1 className="text-xl font-semibold">AI Collaboration Studio</h1>
        </div>

        <div className="flex-1 p-4">
          <DocumentEditor
            document={document}
            onChange={handleDocumentChange}
            onCursorMove={handleCursorMove}
            users={users}
          />
        </div>
      </div>

      {/* Sidebar */}
      <div className="w-80 bg-white border-l flex flex-col">
        {/* User Presence */}
        <div className="p-4 border-b">
          <h3 className="font-semibold mb-2">Online Users</h3>
          <UserPresence users={users} currentUser={currentUser} />
        </div>

        {/* AI Assistant */}
        <div className="flex-1 p-4">
          <AIWritingAssistant
            document={document}
            onSuggestion={(suggestion) => {
              // Handle AI suggestions
              console.log('AI Suggestion:', suggestion)
            }}
          />
        </div>
      </div>
    </div>
  )
}
```

## Database Schema and API Setup

```typescript
// lib/prisma/schema.prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  image     String?
  posts     Post[]
  tickets   SupportTicket[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String   @db.Text
  status    String   @default("draft")
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model SupportTicket {
  id           String   @id @default(cuid())
  title        String
  description  String   @db.Text
  status       String   @default("open")
  priority     String   @default("medium")
  category     String?
  customerName String
  customerEmail String
  assigneeId   String?
  assignee     User?    @relation(fields: [assigneeId], references: [id])
  tags         String[]
  messages     TicketMessage[]
  createdAt    DateTime @default(now())
  updatedAt    DateTime @updatedAt
}

model TicketMessage {
  id        String        @id @default(cuid())
  content   String        @db.Text
  senderId  String
  sender    User          @relation(fields: [senderId], references: [id])
  ticketId  String
  ticket    SupportTicket @relation(fields: [ticketId], references: [id])
  createdAt DateTime      @default(now())
}
```

## Authentication Setup

```typescript
// lib/auth.ts
import { NextAuthOptions } from 'next-auth'
import { PrismaAdapter } from '@next-auth/prisma-adapter'
import { prisma } from '@/lib/prisma'
import CredentialsProvider from 'next-auth/providers/credentials'

export const authOptions: NextAuthOptions = {
  adapter: PrismaAdapter(prisma),
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        const user = await prisma.user.findUnique({
          where: { email: credentials.email }
        })

        if (!user) {
          return null
        }

        // In production, verify password hash
        const isValid = credentials.password === 'password' // Placeholder

        if (!isValid) {
          return null
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
        }
      }
    })
  ],
  session: {
    strategy: 'jwt'
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.id as string
      }
      return session
    }
  }
}
```

## What We've Accomplished

Outstanding! 🎉 You've built complete full-stack AI applications:

1. **AI Blog Platform** - Content creation with AI assistance
2. **AI Support System** - Intelligent customer support with triage
3. **Real-time Collaboration** - Multi-user AI writing studio
4. **Database Integration** - Prisma ORM with proper schemas
5. **Authentication** - NextAuth.js setup for user management
6. **API Routes** - RESTful APIs with proper error handling
7. **Real-time Features** - Socket.IO for live collaboration
8. **Production Ready** - Scalable architecture and best practices

## Next Steps

Ready for production deployment? In [Chapter 8: Production Deployment](08-production-deployment.md), we'll deploy these applications to Vercel with monitoring, scaling, and optimization!

---

**Practice what you've learned:**
1. Add user roles and permissions to your applications
2. Implement real-time notifications for AI events
3. Add analytics and usage tracking
4. Create admin dashboards for managing AI applications
5. Implement AI model versioning and A/B testing

*What full-stack AI application will you build next?* 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `className`, `text`, `error` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Next.js Applications` as an operating subsystem inside **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `post`, `gray`, `user` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Next.js Applications` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `className`.
2. **Input normalization**: shape incoming data so `text` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `error`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [AI SDK Repository](https://github.com/vercel/ai)
  Why it matters: authoritative reference on `AI SDK Repository` (github.com).
- [AI SDK Releases](https://github.com/vercel/ai/releases)
  Why it matters: authoritative reference on `AI SDK Releases` (github.com).
- [AI SDK Docs](https://ai-sdk.dev)
  Why it matters: authoritative reference on `AI SDK Docs` (ai-sdk.dev).

Suggested trace strategy:
- search upstream code for `className` and `text` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: React Integration](06-react-integration.md)
- [Next Chapter: Chapter 8: Production Deployment](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
