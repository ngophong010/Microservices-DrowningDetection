'use client'

import { signIn } from "next-auth/react"
import { Button } from "@/components/ui/button"

export function LoginButton() {
    return (
    <Button
      onClick={() => signIn()}
      className="bg-blue-600 hover:bg-blue-700 text-white"
    >
      Log In
    </Button>
  )
}