import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

interface LoginRequest {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface User {
  id: string;
  username: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'https://urban-space-adventure-45qjwrjvvj5379w7-8000.app.github.dev/api';
  private tokenKey = 'auth_token';
  private userKey = 'auth_user';
  private isBrowser: boolean;

  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  private userSubject = new BehaviorSubject<User | null>(null);
  public user$ = this.userSubject.asObservable();

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) platformId: object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
    this.userSubject.next(this.getStoredUser());
    this.checkAuthStatus();
  }

  private hasToken(): boolean {
    if (!this.isBrowser) {
      return false;
    }

    return !!localStorage.getItem(this.tokenKey);
  }

  private getStoredUser(): User | null {
    if (!this.isBrowser) {
      return null;
    }

    const user = localStorage.getItem(this.userKey);
    return user ? (JSON.parse(user) as User) : null;
  }

  private checkAuthStatus(): void {
    const token = this.getToken();
    this.isAuthenticatedSubject.next(!!token);
  }

  login(username: string, password: string): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(`${this.apiUrl}/auth/login`, {
        username,
        password,
      })
      .pipe(
        tap((response) => {
          this.setToken(response.access_token);
          this.setUser(response.user);
          this.isAuthenticatedSubject.next(true);
          this.userSubject.next(response.user);
        })
      );
  }

  logout(): void {
    if (!this.isBrowser) {
      return;
    }

    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
    this.isAuthenticatedSubject.next(false);
    this.userSubject.next(null);
  }

  getToken(): string | null {
    if (!this.isBrowser) {
      return null;
    }

    return localStorage.getItem(this.tokenKey);
  }

  setToken(token: string): void {
    if (!this.isBrowser) {
      return;
    }

    localStorage.setItem(this.tokenKey, token);
  }

  setUser(user: User): void {
    if (!this.isBrowser) {
      return;
    }

    localStorage.setItem(this.userKey, JSON.stringify(user));
  }

  isAuthenticated(): boolean {
    return this.hasToken();
  }

  getUser(): User | null {
    return this.getStoredUser();
  }
}
