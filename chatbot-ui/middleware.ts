import { NextRequest, NextResponse } from 'next/server';
import { isAuthenticated } from '@/services/auth-service';

export function middleware(request: NextRequest) {
  if (isAuthenticated()) {
    return NextResponse.next();
  }

  return NextResponse.redirect(new URL('/login', request.url));
}

// Define matching paths. This needs to match everything except /login
// (there's probably a smarter pattern for this but for now this'll do)
export const config = {
  matcher: ['/chatbot', '/'],
};
