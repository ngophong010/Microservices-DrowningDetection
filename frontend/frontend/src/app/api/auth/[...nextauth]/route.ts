import NextAuth from "next-auth"
import Cognito from "next-auth/providers/cognito"
import GoogleProvider from "next-auth/providers/google"

const handler = NextAuth({
    providers: [
        CognitoProvider({
            clientId: process.env.COGNITO_CLIENT_ID,
            clientSecret: process.env.COGNITO_CLIENT_SECRET,
            issuer: process.env.COGNITO_ISSUER,
        }),
    ],
    secret: process.env.NEXTAUTH_SECRET,
})

export { handler as GET, handler as POST }