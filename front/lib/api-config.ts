export const API_CONFIG = {
  host: process.env.NEXT_PUBLIC_API_HOST || '46.173.24.165',
  port: process.env.NEXT_PUBLIC_API_PORT || '8000',
  get baseUrl() {
    return `http://${this.host}:${this.port}`;
  }
};

export type ApiError = {
  detail: string;
  status_code: number;
};

export class ApiException extends Error {
  constructor(public error: ApiError) {
    super(error.detail);
    this.name = 'ApiException';
  }
}

export const handleApiError = async (response: Response) => {
  const error = await response.json();
  throw new ApiException(error);
};

export const fetcher = async (url: string) => {
  const response = await fetch(`${API_CONFIG.baseUrl}${url}`);
  if (!response.ok) {
    await handleApiError(response);
  }
  return response.json();
}; 