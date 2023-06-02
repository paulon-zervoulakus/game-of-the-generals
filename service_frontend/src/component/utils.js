import Cookies from "js-cookie";

export function setAccessTokenCookie(accessToken, expirationMinutes) {
    const expirationDate = new Date();
    expirationDate.setTime(expirationDate.getTime() + expirationMinutes * 60 * 1000);
    Cookies.set("access_token", accessToken, {  expires: expirationDate  });
    
}
export function getAccessTokenFromCookie() {
    return Cookies.get("access_token");
}
export function removeAccessTokenCookie() {
    Cookies.remove("access_token");
}