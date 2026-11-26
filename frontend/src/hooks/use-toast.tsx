import React, { createContext, useCallback, useContext, useState } from 'react'

type ToastInput = {
  title: string
  description?: string
  variant?: 'default' | 'destructive'
}

type ToastItem = ToastInput & { id: number }

const ToastContext = createContext<(toast: ToastInput) => void>(() => undefined)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([])

  const toast = useCallback((input: ToastInput) => {
    const id = Date.now() + Math.random()
    setToasts((current) => [...current, { ...input, id }])
    window.setTimeout(() => setToasts((current) => current.filter((t) => t.id !== id)), 5000)
  }, [])

  return (
    <ToastContext.Provider value={toast}>
      {children}
      <div className="fixed bottom-4 right-4 z-50 flex w-80 flex-col gap-2" aria-live="polite">
        {toasts.map((item) => (
          <div
            key={item.id}
            className={`rounded-lg border p-4 shadow-lg animate-fade-in ${item.variant === 'destructive'
              ? 'border-destructive/40 bg-destructive/10 text-destructive'
              : 'border-border bg-card text-card-foreground'}`}
          >
            <p className="text-sm font-semibold">{item.title}</p>
            {item.description && <p className="mt-1 text-sm opacity-80">{item.description}</p>}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export const useToast = () => ({ toast: useContext(ToastContext) })
