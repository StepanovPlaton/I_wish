import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { IonInput } from '@ionic/angular';
import { AuthService } from 'src/app/shared/services/auth.service';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss'],
})
export class RegistrationComponent implements OnInit {
  @ViewChild('loginInput') loginInput: IonInput | undefined;
  @ViewChild('passwordInput') passwordInput: IonInput | undefined;
  @ViewChild('invitationInput') invitationInput: IonInput | undefined;

  registrationFailed: boolean = false;

  constructor(
    private readonly authService: AuthService,
    private readonly cdr: ChangeDetectorRef,
    private readonly router: Router
  ) {}

  ngOnInit() {}

  registration() {
    if (this.registrationFailed) return;
    if (
      (this.loginInput?.value?.toString().length ?? 0) < 3 ||
      (this.passwordInput?.value?.toString().length ?? 0) < 3 ||
      this.invitationInput?.value?.toString() !== '!nvati0nTo!Wish'
    ) {
      this.registrationFailed = true;
      this.setNormalColorsTimeout();
      return;
    }

    this.authService
      .registrationUser({
        login: this.loginInput?.value?.toString() ?? '',
        password: this.passwordInput?.value?.toString() ?? '',
      })
      .subscribe((result) => {
        if (!result) {
          this.registrationFailed = true;
          this.setNormalColorsTimeout();
          if (this.passwordInput) this.passwordInput.value = '';
        } else {
          this.router.navigate(['/']);
        }
      });
  }

  setNormalColorsTimeout() {
    setTimeout(() => {
      this.registrationFailed = false;
      this.cdr.markForCheck();
    }, 3000);
  }
}
