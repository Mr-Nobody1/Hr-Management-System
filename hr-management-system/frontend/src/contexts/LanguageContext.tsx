import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface Language {
  code: string
  name: string
  native_name: string
  flag: string
  rtl: boolean
}

interface Translations {
  [key: string]: string
}

interface LanguageContextType {
  language: string
  setLanguage: (code: string) => void
  languages: Language[]
  translations: Translations
  t: (key: string) => string
  isRTL: boolean
}

const defaultTranslations: Translations = {
  welcome: "Welcome to HR Assistant",
  ask_anything: "Ask me anything about HR...",
  send: "Send",
  quick_actions: "Quick Actions",
  agents_online: "Agents Online",
  powered_by: "Powered by",
  my_payslip: "My Payslip",
  leave_balance: "Leave Balance",
  my_profile: "My Profile",
  clock_in: "Clock In",
  my_benefits: "My Benefits",
  my_team: "My Team",
  performance: "Performance",
  policies: "Policies",
  select_language: "Select Language"
}

const LanguageContext = createContext<LanguageContextType | null>(null)

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState(() => {
    return localStorage.getItem('hr-language') || 'en'
  })
  const [languages, setLanguages] = useState<Language[]>([])
  const [translations, setTranslations] = useState<Translations>(defaultTranslations)
  const [isRTL, setIsRTL] = useState(false)

  // Fetch available languages
  useEffect(() => {
    fetch('/api/languages')
      .then(res => res.json())
      .then(data => {
        setLanguages(data.languages || [])
      })
      .catch(() => {
        // Fallback languages if API fails
        setLanguages([
          { code: 'en', name: 'English', native_name: 'English', flag: '🇬🇧', rtl: false },
          { code: 'es', name: 'Spanish', native_name: 'Español', flag: '🇪🇸', rtl: false },
          { code: 'fr', name: 'French', native_name: 'Français', flag: '🇫🇷', rtl: false },
          { code: 'ar', name: 'Arabic', native_name: 'العربية', flag: '🇸🇦', rtl: true },
          { code: 'zh', name: 'Chinese', native_name: '中文', flag: '🇨🇳', rtl: false },
        ])
      })
  }, [])

  // Fetch translations when language changes
  useEffect(() => {
    fetch(`/api/translations/${language}`)
      .then(res => res.json())
      .then(data => {
        setTranslations({ ...defaultTranslations, ...data })
      })
      .catch(() => {
        setTranslations(defaultTranslations)
      })
    
    // Update RTL setting
    const langInfo = languages.find(l => l.code === language)
    setIsRTL(langInfo?.rtl || false)
    
    // Save to localStorage
    localStorage.setItem('hr-language', language)
    
    // Update document direction
    document.documentElement.dir = langInfo?.rtl ? 'rtl' : 'ltr'
  }, [language, languages])

  const setLanguage = (code: string) => {
    setLanguageState(code)
  }

  const t = (key: string): string => {
    return translations[key] || defaultTranslations[key] || key
  }

  return (
    <LanguageContext.Provider value={{ 
      language, 
      setLanguage, 
      languages, 
      translations, 
      t,
      isRTL 
    }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
}
