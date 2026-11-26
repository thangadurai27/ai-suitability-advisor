import { NavLink, Outlet, Link } from 'react-router-dom'
import {
  BarChart3,
  FileText,
  GraduationCap,
  History,
  Home,
  Library,
  Search,
  Settings,
  ShieldCheck,
} from 'lucide-react'

const navigation = [
  { to: '/', label: 'Home', icon: Home, end: true },
  { to: '/dashboard', label: 'Dashboard', icon: BarChart3 },
  { to: '/analyze', label: 'Analyze', icon: Search },
  { to: '/library', label: 'Library', icon: Library },
  { to: '/history', label: 'History', icon: History },
  { to: '/reports', label: 'Reports', icon: FileText },
  { to: '/learning-center', label: 'Learn', icon: GraduationCap },
  { to: '/settings', label: 'Settings', icon: Settings },
]

export default function Layout() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6">
          <Link to="/" className="flex items-center gap-2 font-semibold tracking-tight">
            <ShieldCheck className="h-6 w-6 text-primary" />
            <span>AI Suitability Advisor</span>
          </Link>
          <nav className="flex flex-wrap items-center gap-1" aria-label="Main navigation">
            {navigation.map(({ to, label, icon: Icon, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  `flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-sm transition-colors ${
                    isActive ? 'bg-primary/15 text-primary' : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                  }`
                }
              >
                <Icon className="h-4 w-4" />
                <span className="hidden sm:inline">{label}</span>
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <Outlet />
      </main>

      <footer className="border-t border-border py-4 text-center text-xs text-muted-foreground">
        Demo mode · No registration required · Rule-based explainable decisions
      </footer>
    </div>
  )
}
