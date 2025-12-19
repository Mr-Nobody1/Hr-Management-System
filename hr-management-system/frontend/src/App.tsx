import { useState, useEffect } from 'react'
import { useTheme } from './hooks/useTheme'
import { LanguageProvider } from './contexts/LanguageContext'
import ThemeToggle from './components/ThemeToggle'
import LanguageSelector from './components/LanguageSelector'
import Sidebar from './components/Sidebar'
import ChatInterface from './components/ChatInterface'

const DEFAULT_EMPLOYEE = {
  id: 'EMP001',
  name: 'John Smith'
}

// Generate a unique session ID for this browser session
const getSessionId = () => {
  let sessionId = sessionStorage.getItem('hr-session-id')
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    sessionStorage.setItem('hr-session-id', sessionId)
  }
  return sessionId
}

function AppContent() {
  const { theme, toggleTheme } = useTheme()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [triggerMessage, setTriggerMessage] = useState<string | null>(null)
  const [sessionId] = useState(getSessionId)

  const handleQuickAction = (query: string) => {
    setTriggerMessage(query)
    setTimeout(() => setTriggerMessage(null), 100)
  }

  return (
    <div className="h-screen flex bg-gradient-to-br from-slate-50 via-slate-100 to-indigo-50 dark:from-[#0f0f23] dark:via-[#0f0f23] dark:to-[#1a1a35] transition-all duration-500">
      {/* Decorative background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-indigo-400/20 to-purple-400/20 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-blue-400/20 to-indigo-400/20 rounded-full blur-3xl" />
      </div>

      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 fixed lg:relative z-20 transition-transform duration-300 ease-out`}>
        <Sidebar
          employeeName={DEFAULT_EMPLOYEE.name}
          employeeId={DEFAULT_EMPLOYEE.id}
          onQuickAction={handleQuickAction}
          onClose={() => setSidebarOpen(false)}
        />
      </div>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/40 backdrop-blur-sm z-10"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden relative z-0">
        {/* Header */}
        <header className="h-16 glass border-b border-white/20 dark:border-white/5 flex items-center justify-between px-4 lg:px-6">
          {/* Mobile menu */}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="lg:hidden p-2.5 rounded-xl bg-white/50 dark:bg-white/5 hover:bg-white dark:hover:bg-white/10 transition-all"
          >
            <svg className="w-5 h-5 text-slate-600 dark:text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Center - Title (mobile) */}
          <div className="lg:hidden">
            <h1 className="font-bold gradient-text">HR Assistant</h1>
          </div>

          <div className="hidden lg:block" />

          {/* Right side */}
          <div className="flex items-center gap-3">
            {/* Status */}
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
              <div className="w-2 h-2 rounded-full bg-emerald-500 status-dot" />
              <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400">Connected</span>
            </div>
            
            {/* Language selector */}
            <LanguageSelector />
            
            {/* Theme toggle */}
            <ThemeToggle theme={theme} onToggle={toggleTheme} />
          </div>
        </header>

        {/* Chat Area */}
        <main className="flex-1 overflow-hidden">
          <ChatInterface 
            employeeId={DEFAULT_EMPLOYEE.id} 
            triggerMessage={triggerMessage}
            sessionId={sessionId}
          />
        </main>
      </div>
    </div>
  )
}

function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  )
}

export default App
