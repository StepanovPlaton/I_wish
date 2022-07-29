import { Component } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { map } from 'rxjs';
import { AVATAR, LOGO } from './shared/consts/images.consts';
import { IUser } from './shared/models/user.models';
import { ApiService } from './shared/services/api.service';
import { AuthService } from './shared/services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  LOGO = LOGO;
  AVATAR = AVATAR;

  userInfo: IUser | null = null;
  showAvatar: boolean = false;

  constructor(
    private readonly translateService: TranslateService,
    private readonly router: Router,
    private readonly apiService: ApiService,
    private readonly authService: AuthService,
   ) {
    this.translateService.setDefaultLang('ru');
    this.translateService.use('ru');

    

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.showAvatar = !event.url.includes("auth")
        if(this.authService.userAuthorizationData && this.showAvatar) {
          this.apiService.getUserInfo(
            this.authService.userAuthorizationData.login
          ).subscribe(
            userInfo => this.userInfo = userInfo
          )
        }
      }
    });
  }

  toRoot() {
    this.router.navigate([""])
  }

  openProfile() {
    this.router.navigate(["profile", this.userInfo?.Login])
  }
}
