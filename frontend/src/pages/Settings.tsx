import { useEffect, useState } from 'react'
import { Check, Moon, Sun } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useToast } from '@/hooks/use-toast'
import { api } from '@/services/api'

export default function Settings() {
  const { toast } = useToast()
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  const [notifications, setNotifications] = useState(true)
  const [apiStatus, setApiStatus] = useState('Checking…')

  useEffect(() => {
    const stored = localStorage.getItem('preferred-theme')
    const initial = stored === 'dark' ? 'dark' : 'light'
    setTheme(initial)
    document.documentElement.classList.toggle('dark', initial === 'dark')
    document.documentElement.setAttribute('data-theme', initial)
    setNotifications(localStorage.getItem('notifications') !== 'false')
    api.healthCheck()
      .then((health) => setApiStatus(`${health.status} (v${health.version})`))
      .catch(() => setApiStatus('Offline — start the backend'))
  }, [])

  const chooseTheme = (next: 'light' | 'dark') => {
    setTheme(next)
    document.documentElement.classList.toggle('dark', next === 'dark')
    document.documentElement.setAttribute('data-theme', next)
    localStorage.setItem('preferred-theme', next)
    toast({ title: 'Theme updated', description: `${next === 'dark' ? 'Dark' : 'Light'} mode enabled.` })
  }

  const toggleNotifications = () => {
    const next = !notifications
    setNotifications(next)
    localStorage.setItem('notifications', String(next))
    toast({ title: 'Notifications updated', description: next ? 'Enabled' : 'Disabled' })
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 sm:px-6 lg:px-8">
      <header>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="mt-1 text-sm text-muted-foreground">Preferences for this browser.</p>
      </header>

      <Card className="mt-8">
        <CardHeader><CardTitle>Appearance</CardTitle></CardHeader>
        <CardContent>
          <p className="mb-3 text-sm text-muted-foreground">Theme</p>
          <div className="flex gap-3">
            <Button variant={theme === 'light' ? 'primary' : 'outline'} onClick={() => chooseTheme('light')}>
              <Sun className="h-4 w-4" /> Light {theme === 'light' && <Check className="h-4 w-4" />}
            </Button>
            <Button variant={theme === 'dark' ? 'primary' : 'outline'} onClick={() => chooseTheme('dark')}>
              <Moon className="h-4 w-4" /> Dark {theme === 'dark' && <Check className="h-4 w-4" />}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader><CardTitle>Notifications</CardTitle></CardHeader>
        <CardContent>
          <label className="flex cursor-pointer items-center gap-3">
            <input type="checkbox" className="h-4 w-4 accent-current" checked={notifications} onChange={toggleNotifications} />
            <span className="text-sm">Show in-app notifications after analyses</span>
          </label>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader><CardTitle>About</CardTitle></CardHeader>
        <CardContent className="space-y-2 text-sm text-muted-foreground">
          <p>AI Suitability Advisor v1.0.0</p>
          <p>Backend API: {apiStatus}</p>
          <p>Demo mode requires no account. All analyses are stored in the shared demo workspace.</p>
        </CardContent>
      </Card>
    </div>
  )
}
