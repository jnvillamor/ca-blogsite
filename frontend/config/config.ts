export const config = {
  apiEndpoint: process.env.API_ENDPOINT || "http://localhost:8000",
  apiVersion: process.env.API_VERSION || "v1",
  sessionMaxAge: process.env.SESSION_MAX_AGE ? parseInt(process.env.SESSION_MAX_AGE) : 60 * 60, 
}