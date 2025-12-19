import { useState, useRef, useEffect } from 'react'
import { useLanguage } from '../contexts/LanguageContext'

interface Language {
  code: string
  name: string
  native_name: string
  flag: string
  rtl: boolean
}

export default function LanguageSelector() {
  const { language, setLanguage, languages } = useLanguage()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const currentLang = languages.find(l => l.code === language) || languages[0]

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  if (languages.length === 0) return null

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-xl
                   bg-white/50 dark:bg-white/5 hover:bg-white dark:hover:bg-white/10
                   border border-white/20 dark:border-white/5
                   transition-all duration-300 group"
        aria-label="Select language"
      >
        <span className="text-lg">{currentLang?.flag}</span>
        <span className="text-sm font-medium text-slate-600 dark:text-slate-300 hidden sm:inline">
          {currentLang?.code.toUpperCase()}
        </span>
        <svg 
          className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 rounded-xl glass border border-white/20 dark:border-white/10 shadow-xl z-50 overflow-hidden animate-fade-in">
          <div className="py-1">
            {languages.map((lang: Language) => (
              <button
                key={lang.code}
                onClick={() => {
                  setLanguage(lang.code)
                  setIsOpen(false)
                }}
                className={`w-full flex items-center gap-3 px-4 py-2.5 text-left
                           hover:bg-indigo-500/10 transition-colors
                           ${language === lang.code ? 'bg-indigo-500/10' : ''}`}
              >
                <span className="text-lg">{lang.flag}</span>
                <div className="flex-1">
                  <p className="text-sm font-medium text-slate-700 dark:text-slate-200">
                    {lang.native_name}
                  </p>
                  <p className="text-xs text-slate-400">
                    {lang.name}
                  </p>
                </div>
                {language === lang.code && (
                  <svg className="w-4 h-4 text-indigo-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
