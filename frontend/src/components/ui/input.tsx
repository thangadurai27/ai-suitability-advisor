import React from 'react'

export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string
  as?: 'input' | 'textarea'
  rows?: number
}

export function Input({ label, as = 'input', rows = 4, className = '', ...props }: InputProps) {
  const fieldClass = `w-full rounded-md border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ${className}`
  return (
    <label className="block space-y-1.5">
      {label && <span className="block text-sm font-medium">{label}</span>}
      {as === 'textarea' ? (
        <textarea {...(props as React.TextareaHTMLAttributes<HTMLTextAreaElement>)} rows={rows} className={fieldClass} />
      ) : (
        <input {...props} className={fieldClass} />
      )}
    </label>
  )
}

export default Input
