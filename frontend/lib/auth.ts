import { config } from "@/config/config"
import { AuthException } from "@/config/exceptions"
import { loginUser, logout, refreshToken } from "@/data-access/auth/auth.data-access"
import { jwtDecode } from "jwt-decode"
import type {
  GetServerSidePropsContext,
  NextApiRequest,
  NextApiResponse,
} from "next"
import type { NextAuthOptions } from "next-auth"
import { getServerSession } from "next-auth/next"
import Credentials from "next-auth/providers/credentials"

type DecodedToken = {
  exp: number
}

const getTokenExp = (token: string): number => {
  const decoded = jwtDecode<DecodedToken>(token)
  return decoded.exp * 1000 // Convert to milliseconds
}

export const authConfig = {
  providers: [
    Credentials({
      name: "Credentials",
      credentials: {
        username: {
          label: "Username",
          type: "text",
          placeholder: "Enter username",
        },
        password: {
          label: "Password",
          type: "password",
          placeholder: "Enter password",
        },
      },
      async authorize(credentials, req) {
        if (!credentials?.username || !credentials?.password) {
          throw new Error("Username and password are required")
        }

        try {
          const response = await loginUser(
            credentials.username,
            credentials.password,
          )
          return {
            id: response.user.id,
            first_name: response.user.first_name,
            last_name: response.user.last_name,
            username: response.user.username,
            avatar: response.user.avatar,
            access_token: response.access_token,
            refresh_token: response.refresh_token,
          }
        } catch (error: any) {
          console.error("Login error:", error)
          throw new Error(
            error instanceof AuthException
              ? error.message
              : "Something went wrong during login",
          )
        }
      },
    }),
  ],
  session: {
    strategy: "jwt",
    maxAge: config.sessionMaxAge,
    updateAge: 24 * 60 * 60, // 24 hours
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.access_token = user.access_token
        token.refresh_token = user.refresh_token
        token.access_token_ttl = getTokenExp(user.access_token)
        token.refresh_token_ttl = getTokenExp(user.refresh_token)

        token.id = user.id
        token.first_name = user.first_name
        token.last_name = user.last_name
        token.username = user.username
        token.avatar = user.avatar

        console.log("New login, token created")
        return token
      }

      if (Date.now() < token.access_token_ttl) {
        console.log("Access token is still valid, returning existing token")
        return token
      }

      if (Date.now() > token.refresh_token_ttl) {
        console.log("Refresh token has expired, returning error")
        return { ...token, error: "RefreshAccessTokenError" }
      }

      const refreshed_token = await refreshToken(token.refresh_token)
      token.id = refreshed_token.user.id
      token.first_name = refreshed_token.user.first_name
      token.last_name = refreshed_token.user.last_name
      token.username = refreshed_token.user.username
      token.avatar = refreshed_token.user.avatar

      token.access_token = refreshed_token.access_token
      token.refresh_token = refreshed_token.refresh_token
      token.access_token_ttl = getTokenExp(refreshed_token.access_token)
      token.refresh_token_ttl = getTokenExp(refreshed_token.refresh_token)

      return token
    },
    async session({ session, token }) {
      session.user.id = token.id
      session.user.first_name = token.first_name
      session.user.last_name = token.last_name
      session.user.username = token.username
      session.user.avatar = token.avatar
      session.access_token = token.access_token

      return session
    },
  },
  events: {
    async signOut({ token }) {
      if (!token?.access_token) return

      await logout(token.access_token)
    },
  },
  pages: {
    signIn: "/login",
  },
} satisfies NextAuthOptions

export function auth(
  ...args:
    | [GetServerSidePropsContext["req"], GetServerSidePropsContext["res"]]
    | [NextApiRequest, NextApiResponse]
    | []
) {
  return getServerSession(...args, authConfig)
}
