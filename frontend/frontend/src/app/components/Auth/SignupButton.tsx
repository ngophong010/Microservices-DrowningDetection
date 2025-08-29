'use client'

import { signIn } from "next-auth/react"
import { Button } from "@/components/ui/button"

export function SignupButton() {
    return (
    <Button
      onClick={() => signIn()} // Same as login; behavior depends on your auth provider
      className="bg-green-600 hover:bg-green-700 text-white"
    >
      Sign Up
    </Button>
  )
}