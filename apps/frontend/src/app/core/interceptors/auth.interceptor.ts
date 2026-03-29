import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const isLoginRequest = req.url.includes('/auth/login');

  const token = authService.getToken();

  if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && !isLoginRequest) {
        authService.logout();

        const currentUrl = router.url || '/';
        if (!currentUrl.startsWith('/login')) {
          router.navigate(['/login'], {
            queryParams: {
              reason: 'session-expired',
              returnUrl: currentUrl,
            },
          });
        }
      }
      return throwError(() => error);
    })
  );
};

