import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { IonInput } from '@ionic/angular';
import { AuthService } from 'src/app/shared/services/auth.service';

@Component({
  selector: 'app-authorization',
  templateUrl: './authorization.component.html',
  styleUrls: ['./authorization.component.scss']
})
export class AuthorizationComponent implements OnInit {
  @ViewChild('loginInput') loginInput: IonInput | undefined;
  @ViewChild('passwordInput') passwordInput: IonInput | undefined;

  authorizationFailed: boolean = false;

  constructor(
    private readonly authService: AuthService,
    private readonly cdr: ChangeDetectorRef,
    private readonly router: Router,
  ) { }

  ngOnInit() {
  }

  authorization() {
    if((this.loginInput?.value?.toString().length ?? 0) < 3 ||
       (this.passwordInput?.value?.toString().length ?? 0) < 3) {
      this.authorizationFailed = true;
      this.setNormalColorsTimeout()
      return
    }

    this.authService.authorizationUser({
      login: this.loginInput?.value?.toString() ?? "",
      password: this.passwordInput?.value?.toString() ?? ""
    }).subscribe(result => {
      if(!result) {
        this.authorizationFailed = true;
        this.setNormalColorsTimeout()
        if(this.passwordInput) this.passwordInput.value = ""
      } else {
        this.router.navigate(["/"])
      }
    })
  }

  setNormalColorsTimeout() {
    setTimeout(() => {
      this.authorizationFailed = false;
      this.cdr.markForCheck()
    }, 1000)
  }

}
