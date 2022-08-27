import {
  AfterViewInit,
  Component,
  ElementRef,
  NgZone,
  ViewChild,
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GestureController, IonModal } from '@ionic/angular';
import { combineLatest, of, switchMap } from 'rxjs';
import { WishListService } from 'src/app/base/wish-list/wish-list.service';
import {
  ADD_IMAGE,
  AVATAR,
  CHECK,
  CLOSE,
  DELETE,
  EDIT,
  EXTERNAL_LINK,
} from 'src/app/shared/consts/images.consts';
import { MAX_IMAGE_SIZE } from 'src/app/shared/consts/settings.consts';
import { IWish } from 'src/app/shared/models/http.model';
import { IUser } from 'src/app/shared/models/user.models';
import { ApiService } from 'src/app/shared/services/api.service';
import { AuthService } from 'src/app/shared/services/auth.service';

@Component({
  selector: 'app-wish',
  templateUrl: './wish.component.html',
  styleUrls: ['./wish.component.scss'],
})
export class WishComponent implements AfterViewInit {
  ADD_IMAGE = ADD_IMAGE;
  EDIT = EDIT;
  EXTERNAL_LINK = EXTERNAL_LINK;
  CHECK = CHECK;
  CLOSE = CLOSE;
  AVATAR = AVATAR;
  DELETE = DELETE;

  wish: IWish = {
    ID: -1,
    Wish: '',
    Description: '',
    Price: -1,
    Link: '',
    Owner: -1,
    Login: '',
    Anonymous: false,
  };
  ownerInfo: IUser | null = null;

  wishFormattedHidingDate: string | null = null;

  owner: boolean = false;

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

  @ViewChild('swipeWrapper') swipeWrapper: ElementRef | undefined;
  @ViewChild('viewImageModal') viewImageModal: IonModal | undefined;
  @ViewChild('setHidingDateModal') setHidingDateModal: IonModal | undefined;

  constructor(
    private readonly activatedRoute: ActivatedRoute,
    private readonly apiService: ApiService,
    private readonly authService: AuthService,
    private readonly router: Router,
    private readonly gestureCtrl: GestureController,
    private readonly wishListService: WishListService,
    private readonly ngZone: NgZone
  ) {
    combineLatest([this.activatedRoute.queryParams, this.activatedRoute.params])
      .pipe(
        switchMap(([query, params]) => {
          if (params['id'] === 'create') {
            this.owner = true;
            if (this.authService.userAuthorizationData)
              return this.apiService.getUserInfo(
                this.authService.userAuthorizationData?.login
              );
            else return of(null);
          } else {
            const wish = query as IWish;
            if (wish) {
              this.wish = {
                ...this.wish,
                ...wish,
                Owner: +wish.Owner,
                ID: +wish.ID,
                Price: +(wish.Price ?? 0),
                Anonymous: query['Anonymous'] === 'true',
              };
              if (this.wish.HidingDate)
                this.wishFormattedHidingDate = new Date(
                  this.wish.HidingDate
                ).toLocaleString();
              if (
                this.wish.Owner === this.authService.userAuthorizationData?.id
              ) {
                this.owner = true;
              }
            } else {
              this.owner = true;
              this.wish = {
                ...this.wish,
                Owner: this.authService.userAuthorizationData?.id ?? -1,
                Login: this.authService.userAuthorizationData?.login ?? '',
              };
            }
            if (this.wish.Login !== '' && this.wish.Owner !== -1)
              return this.apiService.getUserInfo(wish.Login);
            else return of(null);
          }
        })
      )
      .subscribe((ownerInfo) => {
        if (ownerInfo) this.ownerInfo = ownerInfo;
      });
  }

  ngAfterViewInit(): void {
    if (this.viewImageModal)
      this.viewImageModal.cssClass = ['modal', 'view-image-modal'];
    if (this.setHidingDateModal)
      this.setHidingDateModal.cssClass = ['modal', 'set-hiding-date-modal'];

    if (this.swipeWrapper) {
      let gesture = this.gestureCtrl.create({
        gestureName: 'my-gesture',
        el: this.swipeWrapper.nativeElement,
        onMove: (details) => {
          if (details.deltaX > 100) {
            const nextWish = this.wishListService.getNextWish(this.wish.ID);
            if (!nextWish) {
              this.error = true;
              return;
            }
            this.ngZone.run(() => {
              this.router.navigate(['wish', nextWish.ID], {
                queryParams: { ...nextWish },
              });
            });
          } else if (details.deltaX < -100) {
            const previousWish = this.wishListService.getNextWish(this.wish.ID);
            if (!previousWish) {
              this.error = true;
              return;
            }

            this.ngZone.run(() => {
              this.router.navigate(['wish', previousWish.ID], {
                queryParams: { ...previousWish },
              });
            });
          }
        },
      });
      gesture.enable();
    }
  }

  closeViewImageModal() {
    if (this.viewImageModal) this.viewImageModal.dismiss();
  }

  openOwner() {
    if (this.ownerInfo) {
      this.router.navigate(['profile', this.ownerInfo.Login]);
    }
  }

  deleteWish() {
    if (this.authService.userAuthorizationData) {
      this.apiService
        .deleteWish(this.authService.userAuthorizationData, this.wish.ID)
        .subscribe(() => this.close());
    }
  }

  submit() {
    if (this.wish.Wish.length < 3) {
      this.error = true;
      return;
    }

    if (this.authService.userAuthorizationData) {
      if (this.wish.ID === -1) {
        this.apiService
          .createWish(this.authService.userAuthorizationData, this.wish)
          .subscribe(() => {
            this.close();
          });
      } else {
        this.apiService
          .updateWish(this.authService.userAuthorizationData, this.wish)
          .subscribe(() => {
            this.close();
          });
      }
    }
  }

  close() {
    this.router.navigate(['']);
  }

  openLink(link: string | undefined) {
    if (link) window.open(link);
  }

  onWishNameChange(event: Event) {
    this.wish.Wish = (event.target as HTMLInputElement).value;
  }
  onWishDescriptionChange(event: Event) {
    this.wish.Description = (event.target as HTMLInputElement).value;
  }
  onWishPriceChange(event: Event) {
    this.wish.Price = +(event.target as HTMLInputElement).value;
  }
  onWishLinkChange(event: Event) {
    this.wish.Link = (event.target as HTMLInputElement).value;
  }
  onWishImageChange(event: any) {
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
          this.wish.Image = reader.result?.toString();
        };
        reader.onerror = () => {
          this.error = true;
          return;
        };
      }
    } else this.error = true;
  }
  onWishAnonymouslyChange(event: Event) {
    this.wish.Anonymous = (event as CustomEvent).detail.checked;
  }
  onWishHidingDateChange(event: Event) {
    setTimeout(() => {
      this.setHidingDateModal?.dismiss();
    }, 300);
    this.wish.HidingDate = (event as CustomEvent).detail.value;
    if (this.wish.HidingDate)
      this.wishFormattedHidingDate = new Date(
        this.wish.HidingDate
      ).toLocaleString();
  }
}
