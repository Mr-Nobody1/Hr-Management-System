import { useLanguage } from '../contexts/LanguageContext'

interface QuickAction {
  label: string
  labelKey: string
  query: string
  icon: JSX.Element
  gradient: string
}

interface SidebarProps {
  employeeName: string
  employeeId: string
  onQuickAction: (query: string) => void
  onClose?: () => void
}

// Icon components
const PayslipIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
)

const LeaveIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
)

const ProfileIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
)

const ClockIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
)

const BenefitsIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7" />
  </svg>
)

const TeamIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
  </svg>
)

const PerformanceIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
  </svg>
)

const PolicyIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
)

const quickActions: QuickAction[] = [
  { label: 'My Payslip', labelKey: 'my_payslip', query: 'Show my payslip', icon: <PayslipIcon />, gradient: 'from-emerald-500 to-teal-500' },
  { label: 'Leave Balance', labelKey: 'leave_balance', query: 'What is my leave balance?', icon: <LeaveIcon />, gradient: 'from-blue-500 to-cyan-500' },
  { label: 'My Profile', labelKey: 'my_profile', query: 'Show my profile', icon: <ProfileIcon />, gradient: 'from-violet-500 to-purple-500' },
  { label: 'Clock In', labelKey: 'clock_in', query: 'Clock in', icon: <ClockIcon />, gradient: 'from-orange-500 to-amber-500' },
  { label: 'My Benefits', labelKey: 'my_benefits', query: 'What benefits do I have?', icon: <BenefitsIcon />, gradient: 'from-pink-500 to-rose-500' },
  { label: 'My Team', labelKey: 'my_team', query: 'Who is in my team?', icon: <TeamIcon />, gradient: 'from-indigo-500 to-blue-500' },
  { label: 'Performance', labelKey: 'performance', query: 'Show my performance review', icon: <PerformanceIcon />, gradient: 'from-yellow-500 to-orange-500' },
  { label: 'Policies', labelKey: 'policies', query: 'Show company policies', icon: <PolicyIcon />, gradient: 'from-slate-500 to-gray-600' },
]

export default function Sidebar({ employeeName, employeeId, onQuickAction, onClose }: SidebarProps) {
  const { t } = useLanguage()
  const initials = employeeName.split(' ').map(n => n[0]).join('')
  
  return (
    <aside className="w-72 h-screen glass border-r border-white/20 dark:border-white/5 flex flex-col">
      {/* Header */}
      <div className="p-5 border-b border-white/10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30 animate-float">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h1 className="font-bold text-slate-800 dark:text-white">HR Assistant</h1>
              <p className="text-xs text-slate-500 dark:text-slate-400">AI-Powered</p>
            </div>
          </div>
          {onClose && (
            <button onClick={onClose} className="lg:hidden p-2 hover:bg-white/50 dark:hover:bg-white/5 rounded-lg transition-colors">
              <svg className="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Employee Card */}
      <div className="p-5">
        <div className="p-4 rounded-2xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-indigo-500/20">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg shadow-lg">
              {initials}
            </div>
            <div>
              <h3 className="font-semibold text-slate-800 dark:text-white">{employeeName}</h3>
              <p className="text-sm text-indigo-600 dark:text-indigo-400">{employeeId}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex-1 px-5 pb-5 overflow-y-auto">
        <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
          <span className="w-8 h-px bg-gradient-to-r from-indigo-500 to-transparent" />
          {t('quick_actions')}
        </h4>
        <div className="space-y-2">
          {quickActions.map((action, index) => (
            <button
              key={action.label}
              onClick={() => onQuickAction(action.query)}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-xl
                         bg-white/50 dark:bg-white/5 hover:bg-white dark:hover:bg-white/10
                         border border-transparent hover:border-indigo-500/30
                         transition-all duration-300 group card-hover"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className={`w-9 h-9 rounded-lg bg-gradient-to-br ${action.gradient} flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                {action.icon}
              </div>
              <span className="text-sm font-medium text-slate-700 dark:text-slate-200 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                {t(action.labelKey) || action.label}
              </span>
              <svg className="w-4 h-4 text-slate-400 ml-auto opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          ))}
        </div>
      </div>

      {/* Agent Status */}
      <div className="p-5 border-t border-white/10">
        <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-500/10 to-teal-500/10 border border-emerald-500/20">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 status-dot" />
            <span className="text-sm font-semibold text-emerald-600 dark:text-emerald-400">8 {t('agents_online')}</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {['Payslip', 'Leave', 'Employee', 'Attendance', 'Benefits', 'Performance', 'Policy', 'Orchestrator'].map(agent => (
              <span key={agent} className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                {agent}
              </span>
            ))}
          </div>
        </div>
      </div>
    </aside>
  )
}
