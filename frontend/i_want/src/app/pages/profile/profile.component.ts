import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertController } from '@ionic/angular';
import { TranslateService } from '@ngx-translate/core';
import { combineLatest, from, of, pluck, switchMap } from 'rxjs';
import {
  ADD_IMAGE,
  AVATAR,
  CHECK,
  CLOSE,
  EDIT,
  EXTERNAL_LINK,
  LOGOUT,
} from 'src/app/shared/consts/images.consts';
import { MAX_IMAGE_SIZE } from 'src/app/shared/consts/settings.consts';
import { IWish } from 'src/app/shared/models/http.model';
import { IUser } from 'src/app/shared/models/user.models';
import { ApiService } from 'src/app/shared/services/api.service';
import { AuthService } from 'src/app/shared/services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  ADD_IMAGE = ADD_IMAGE;
  EDIT = EDIT;
  EXTERNAL_LINK = EXTERNAL_LINK;
  CHECK = CHECK;
  CLOSE = CLOSE;
  AVATAR = AVATAR;
  LOGOUT = LOGOUT;

  user: IUser = {
    ID: -1,
    Login: '',
  };

  thisIsMe: boolean = false;

  private _error: boolean | undefined = undefined;
  set error(state: boolean | undefined) {
    if (state) {
      setTimeout(() => (this.error = false), 3000);
    }
    this._error = state;
  }
  get error(): boolean | undefined {
    return this._error;
  }

  constructor(
    private readonly activatedRoute: ActivatedRoute,
    private readonly apiService: ApiService,
    private readonly authService: AuthService,
    private readonly router: Router,
    private readonly alertController: AlertController,
    private readonly translateService: TranslateService
  ) {
    this.activatedRoute.params
      .pipe(
        pluck('login'),
        switchMap((Login) => {
          return this.apiService.getUserInfo(Login);
        })
      )
      .subscribe((user) => {
        this.user = {
          ...this.user,
          ...user,
        };
        if (this.authService.userAuthorizationData?.id === user.ID) {
          this.thisIsMe = true;
        }
      });
  }

  ngOnInit() {}

  submit() {
    if (this.authService.userAuthorizationData) {
      this.apiService
        .updateUserInfo(this.authService.userAuthorizationData, this.user)
        .subscribe(
          () => {
            this.close();
          },
          () => (this.error = true)
        );
    }
  }

  close() {
    this.router.navigate(['']);
  }

  logout() {
    this.translateService
      .get(['Logout', 'Cancel'])
      .pipe(
        switchMap((translations) => {
          return from(
            this.alertController.create({
              header: translations.Logout + '?',
              cssClass: ['alert'],
              buttons: [
                {
                  text: translations.Cancel,
                  role: 'cancel',
                },
                {
                  text: translations.Logout,
                  role: 'confirm',
                  handler: () => {
                    this.authService.logout();
                  },
                },
              ],
            })
          );
        })
      )
      .subscribe((alert) => alert.present());
  }

  openTelegramAccount(account: string | undefined) {
    if (account) window.open(`https://t.me/${account.replace('@', '')}`);
  }

  onAboutMeChange(event: Event) {
    this.user.AboutMe = (event.target as HTMLInputElement).value;
  }
  onTelegramAccountChange(event: Event) {
    this.user.Telegram = (event.target as HTMLInputElement).value;
  }
  onProfileAvatarChange(event: any) {
    let files: FileList = event.target.files;
    if (files.length === 1) {
      let file = files[0];
      if (file.size > MAX_IMAGE_SIZE * 1024) {
        this.error = true;
        return;
      } else {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          this.user.Avatar = reader.result?.toString();
        };
        reader.onerror = () => {
          this.error = true;
          return;
        };
      }
    } else this.error = true;
  }
}
