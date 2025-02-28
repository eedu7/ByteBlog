export interface RegisterUserRequest {
    username: string;
    email: string;
    password: string;
}

export interface LoginUserRequest {
    email: string;
    password: string;
}

export interface Token {
    access_token: string;
    refresh_token: string;
    expires_in: number;
    token_type: string;
}

export interface User {
    uuid: string;
    email: string;
    username: string;
}

export interface AuthResponse {
    token: Token;
    user: User;
}
