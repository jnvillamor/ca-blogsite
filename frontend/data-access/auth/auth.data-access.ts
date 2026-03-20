import { config } from "@/config/config";
import { AuthException } from "@/config/exceptions";
import { AuthResponse, RegisterDTO } from "../dto/auth.dto";
import { RegisterData } from "../types/auth.types";

export const loginUser = async (
  username: string,
  password: string,
): Promise<AuthResponse> => {
  const payload = new URLSearchParams({
    username: username,
    password: password,
    grant_type: "password",
  });

  const res = await fetch(
    `${config.apiEndpoint}/${config.apiVersion}/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: payload.toString(),
    },
  );

  if (!res.ok) {
    const data = await res.json();
    throw new AuthException(data.detail || "Login failed");
  }

  const data = await res.json();
  return data as AuthResponse;
};

export const refreshToken = async (refreshToken: string): Promise<AuthResponse> => {
  const response = await fetch(
    `${config.apiEndpoint}/${config.apiVersion}/auth/refresh/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${refreshToken}`,
      },
    },
  )

  if (!response.ok) {
    console.error("Token refresh failed with status:", response.status);
    const data = await response.json();
    throw new AuthException(data.detail || "Token refresh failed");
  }

  const data = await response.json();
  return data as AuthResponse;
}

export const logout = async (accessToken: string): Promise<void> => {
  const response = await fetch(
    `${config.apiEndpoint}/${config.apiVersion}/auth/logout/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`,
      },
    },
  )

  if (!response.ok) {
    console.error("Logout failed with status:", response.status);
    const data = await response.json();
    throw new AuthException(data.detail || "Logout failed");
  }
}

export const registerUser = async (
  data: RegisterData
): Promise<AuthResponse> => {
  const payload: RegisterDTO = {
    first_name: data.first_name,
    last_name: data.last_name,
    username: data.username,
    password: data.password
  }

  const response = await fetch(
    `${config.apiEndpoint}/${config.apiVersion}/users/register`, 
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  if (!response.ok) {
    const data = await response.json();
    throw new AuthException(data.detail || "Registration failed");
  }

  const result = await response.json();
  return result as AuthResponse;
}