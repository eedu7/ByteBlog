export interface RegisterUserRequest {
    username: string;
    email: string;
    password: string;
}

export interface LoginUserRequest {
    email: string;
    password: string;
}

interface TokenResponse {
    access_token: string;
    refresh_token: string;
    expires_in: number;
    token_type: string;
}

interface UserResponse {
    uuid: string;
    email: string;
    username: string;
}

export interface AuthResponse {
    token: TokenResponse;
    user: UserResponse;
}
