import React from 'react'

type DivProps = React.HTMLAttributes<HTMLDivElement>

export function Card({ className = '', ...props }: DivProps) {
  return <div {...props} className={`rounded-xl border border-border bg-card text-card-foreground shadow-sm ${className}`} />
}

export function CardHeader({ className = '', ...props }: DivProps) {
  return <div {...props} className={`flex flex-col gap-1 p-5 ${className}`} />
}

export function CardTitle({ className = '', ...props }: DivProps) {
  return <h3 {...props} className={`text-lg font-semibold leading-tight ${className}`} />
}

export function CardDescription({ className = '', ...props }: DivProps) {
  return <p {...props} className={`text-sm text-muted-foreground ${className}`} />
}

export function CardContent({ className = '', ...props }: DivProps) {
  return <div {...props} className={`p-5 pt-0 ${className}`} />
}

export function CardFooter({ className = '', ...props }: DivProps) {
  return <div {...props} className={`flex items-center p-5 pt-0 ${className}`} />
}
