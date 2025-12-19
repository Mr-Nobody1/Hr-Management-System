import ReactMarkdown from 'react-markdown'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  agentName?: string
  timestamp: string
}

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  
  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true 
    }).toLowerCase()
  }
  
  if (isUser) {
    return (
      <div className="flex justify-end animate-slide-up">
        <div className="flex items-end gap-3 max-w-[80%]">
          <div className="bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-2xl rounded-br-sm px-5 py-3.5 shadow-lg shadow-indigo-500/20">
            <p className="text-[15px] leading-relaxed">{message.content}</p>
            <p className="text-xs text-indigo-200 mt-2 text-right">{formatTime(message.timestamp)}</p>
          </div>
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold shadow-lg flex-shrink-0">
            JS
          </div>
        </div>
      </div>
    )
  }
  
  return (
    <div className="flex justify-start animate-slide-up">
      <div className="flex items-start gap-3 max-w-[85%]">
        {/* AI Avatar */}
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 flex-shrink-0">
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        
        {/* Message Content */}
        <div className="glass rounded-2xl rounded-tl-sm px-5 py-4 shadow-lg">
          {/* Agent Name */}
          {message.agentName && (
            <div className="flex items-center gap-2 mb-3 pb-2 border-b border-indigo-500/10">
              <div className="w-1.5 h-1.5 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500" />
              <span className="text-xs font-semibold gradient-text">
                {message.agentName}
              </span>
            </div>
          )}
          
          {/* Message Text */}
          <div className="markdown-content text-slate-700 dark:text-slate-200 text-[15px]">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
          
          {/* Timestamp */}
          <p className="text-xs text-slate-400 mt-3 flex items-center gap-1">
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {formatTime(message.timestamp)}
          </p>
        </div>
      </div>
    </div>
  )
}
