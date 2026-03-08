import { BasicUserDTO } from "./user";

export interface AuthResponse {
  access_token: string;
  access_token_ttl: number;
  refresh_token: string;
  refresh_token_ttl: number;
  user: BasicUserDTO;
}