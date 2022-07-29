export interface IAuthorizationResponse {
    ID: number
    Token: string
}

export interface IWish  {
    ID: number
    Wish: string
    Image?: string
    Description?: string
    Price?: number
    Link?: string
    Owner: number
    Login: string
    Avatar?: string
}