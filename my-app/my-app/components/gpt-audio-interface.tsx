'use client'

import { useState, useRef, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Mic, Send, Play, Pause, User, Bot } from 'lucide-react'

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  audioFile?: string;
}

export function GptAudioInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentlyPlaying, setCurrentlyPlaying] = useState<string | null>(null)
  const audioRef = useRef<HTMLAudioElement>(null)
  const scrollAreaRef = useRef<HTMLDivElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:5000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: data.response,
        audioFile: data.audio_file
      }

      setMessages(prev => [...prev, aiMessage])

      // Automatically play the latest received audio
      playAudio(aiMessage.id, aiMessage.audioFile!)
    } catch (error) {
      console.error('Error:', error)
      // Handle error (e.g., show an error message to the user)
    } finally {
      setIsLoading(false)
    }
  }

  const playAudio = (id: string, fileName: string) => {
    if (currentlyPlaying === id) {
      audioRef.current?.pause()
      setCurrentlyPlaying(null)
    } else {
      if (audioRef.current) {
        audioRef.current.src = `http://localhost:5000/${fileName}`
        audioRef.current.play()
        setCurrentlyPlaying(id)
      }
    }
  }

  useEffect(() => {
    // Scroll to the bottom when new messages are added
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [messages])

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto p-4">
      <ScrollArea className="flex-grow mb-4 border rounded-md p-4" ref={scrollAreaRef}>
        {messages.map((message) => (
          <div key={message.id} className={`mb-4 p-2 rounded-md ${message.type === 'user' ? 'bg-primary text-primary-foreground' : 'bg-secondary'}`}>
            <div className="flex items-center gap-2 mb-2">
              {message.type === 'user' ? (
                <User className="h-5 w-5" />
              ) : (
                <Bot className="h-5 w-5" />
              )}
              <span className="font-semibold">{message.type === 'user' ? 'You' : 'AI'}</span>
              {message.type === 'ai' && (
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => playAudio(message.id, message.audioFile!)}
                  aria-label={currentlyPlaying === message.id ? "Pause audio" : "Play audio"}
                >
                  {currentlyPlaying === message.id ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                </Button>
              )}
            </div>
            <p className="text-sm">{message.content}</p>
          </div>
        ))}
      </ScrollArea>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <Input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow"
        />
        <Button type="submit" disabled={isLoading}>
          {isLoading ? <Mic className="h-4 w-4 animate-pulse" /> : <Send className="h-4 w-4" />}
          <span className="sr-only">{isLoading ? "Processing" : "Send"}</span>
        </Button>
      </form>
      <audio ref={audioRef} className="hidden" onEnded={() => setCurrentlyPlaying(null)} />
    </div>
  )
}