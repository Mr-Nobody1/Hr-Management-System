import { useState, useRef, useEffect } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import MessageBubble from './MessageBubble'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  agentName?: string
  timestamp: string
}

interface ChatInterfaceProps {
  employeeId: string
  triggerMessage?: string | null
  sessionId: string
}

export default function ChatInterface({ employeeId, triggerMessage, sessionId }: ChatInterfaceProps) {
  const { language, t } = useLanguage()
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: `👋 **Hello!**\n\nI'm your AI-powered HR Assistant. I'm here to help you with:\n\n💰 **Payslip** - View salary and deductions\n📅 **Leave** - Check balance and request time off\n👤 **Profile** - View your information\n⏰ **Attendance** - Clock in/out and records\n🎁 **Benefits** - Health, 401k, and more\n📊 **Performance** - Reviews, goals, and KPIs\n📋 **Policies** - Company rules and FAQs\n\nJust type your question naturally, and I'll understand what you need!`,
      agentName: 'HR Assistant',
      timestamp: new Date().toISOString()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (triggerMessage) {
      sendMessage(triggerMessage)
    }
  }, [triggerMessage])

  const sendMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText.trim(),
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage.content,
          employee_id: employeeId,
          session_id: sessionId,
          language: language
        })
      })

      if (!response.ok) throw new Error('Failed to get response')

      const data = await response.json()

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        agentName: data.agent_name,
        timestamp: data.timestamp
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '❌ Connection error. Please ensure the backend is running on port 8000.',
        agentName: 'System',
        timestamp: new Date().toISOString()
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(input)
  }

  const suggestions = [
    { label: t('my_payslip'), query: "Show my payslip" },
    { label: t('leave_balance'), query: "What is my leave balance?" },
    { label: t('performance'), query: "Show my performance review" },
    { label: t('policies'), query: "What is the WFH policy?" }
  ]

  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.map((message, index) => (
            <div key={message.id} style={{ animationDelay: `${index * 100}ms` }}>
              <MessageBubble message={message} />
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start animate-fade-in">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div className="glass rounded-2xl rounded-tl-sm shadow-lg">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 lg:p-6">
        <div className="max-w-4xl mx-auto">
          {/* Suggestions - show only if no messages yet */}
          {messages.length === 1 && (
            <div className="flex flex-wrap gap-2 mb-4 justify-center animate-fade-in">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion.query}
                  onClick={() => sendMessage(suggestion.query)}
                  className="px-4 py-2 rounded-full text-sm font-medium
                           bg-white/70 dark:bg-white/5 hover:bg-white dark:hover:bg-white/10
                           text-indigo-600 dark:text-indigo-400
                           border border-indigo-500/20 hover:border-indigo-500/40
                           transition-all duration-300 hover:scale-105"
                >
                  {suggestion.label}
                </button>
              ))}
            </div>
          )}

          <form onSubmit={handleSubmit} className="relative">
            <div className="glass rounded-2xl p-2 shadow-xl shadow-indigo-500/5 flex items-center gap-2">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={t('ask_anything')}
                className="flex-1 px-4 py-3 bg-transparent border-0
                         text-slate-800 dark:text-white placeholder-slate-400
                         focus:outline-none text-base"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600
                         text-white font-medium rounded-xl shadow-lg shadow-indigo-500/30
                         disabled:opacity-50 disabled:cursor-not-allowed
                         hover:shadow-xl hover:shadow-indigo-500/40 hover:scale-[1.02]
                         transition-all duration-300 flex items-center gap-2 btn-premium"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                <span className="hidden sm:inline">{t('send')}</span>
              </button>
            </div>
          </form>

          <p className="text-center text-xs text-slate-400 mt-3">
            {t('powered_by')} <span className="gradient-text font-medium">Gemini 2.5 Flash</span> • 8 Specialized Agents
          </p>
        </div>
      </div>
    </div>
  )
}
