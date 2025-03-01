import { NextResponse, type NextRequest } from "next/server";

const protectedRoutes = ["/dashboard"];

export function middleware(req: NextRequest) {
  const access_token = req.cookies.get("access_token");
  if (protectedRoutes.includes(req.nextUrl.pathname) && !access_token) {
    return NextResponse.redirect(new URL("/", req.url));
  }
  return NextResponse.next();
}
