import { BasicUserDTO } from "./user.dto";

export interface AuthResponse {
  access_token: string;
  access_token_ttl: number;
  refresh_token: string;
  refresh_token_ttl: number;
  user: BasicUserDTO;
}

export interface RegisterDTO {
  first_name: string;
  last_name: string;
  username: string;
  password: string;
}