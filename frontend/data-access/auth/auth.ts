import { config } from "@/config/config";
import { AuthException } from "@/config/exceptions";
import { AuthResponse } from "../dto/auth";

export const login = async (
  username: string,
  password: string,
): Promise<AuthResponse> => {
  const payload = new URLSearchParams({
    username: username,
    password: password,
    grant_type: "password",
  });

  console.log("Login payload:", payload.toString());
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
    console.error("Login failed with message:", data.detail || "Unknown error");
    throw new AuthException(data.detail || "Login failed");
  }

  console.log("Login successful, response status:", res.status);
  const data = await res.json();
  return data as AuthResponse;
};

export const refreshToken = async (refreshToken: string): Promise<AuthResponse> => {
  console.log("Refreshing token...");
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

  console.log("Token refresh successful, response status:", response.status);
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

  console.log("Logout successful, response status:", response.status);
}