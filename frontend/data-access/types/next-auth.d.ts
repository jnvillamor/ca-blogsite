import { DefaultSession, DefaultUser } from "next-auth";

declare module "next-auth" {
  interface User extends DefaultUser {
    access_token: string;
    refresh_token: string;

    id: string;
    first_name: string;
    last_name: string;
    username: string;
    avatar?: string;
  }

  interface Session extends DefaultSession {
    user: DefaultSession["user"] & {
      id: string;
      first_name: string;
      last_name: string;
      username: string;
      avatar?: string;
    };
    access_token: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    access_token: string;
    refresh_token: string;
    access_token_ttl: number;
    refresh_token_ttl: number;

    id: string;
    first_name: string;
    last_name: string;
    username: string;
    avatar?: string;

    error?: "RefreshAccessTokenError";
  }
}