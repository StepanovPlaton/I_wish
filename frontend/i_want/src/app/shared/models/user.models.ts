export interface IUserAuthorizationData {
    login: string;
    password: string;
}
export interface IUserAuthorizationResponse {
    id: number
    token: string
}

export interface IUser {
    ID: number
    Login: string
    Avatar?: string
    AboutMe?: string
    Telegram?: string
}