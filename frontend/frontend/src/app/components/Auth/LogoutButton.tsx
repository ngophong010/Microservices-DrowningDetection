'use client'

import { signOut } from "next-auth/react"
import { Button } from "@/components/ui/button"

export function LogoutButton() {
    return (
        <Button
            onClick={() => signOut()}
            className="bg-red-600 hover:bg-red-700 text-white"
        >
            Log Out
        </Button>
    )
}