import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { of, pluck, switchMap } from 'rxjs';
import { ADD_IMAGE, AVATAR, CHECK, CLOSE, DELETE, EDIT, EXTERNAL_LINK } from 'src/app/shared/consts/images.consts';
import { MAX_IMAGE_SIZE } from 'src/app/shared/consts/settings.consts';
import { IWish } from 'src/app/shared/models/http.model';
import { IUser } from 'src/app/shared/models/user.models';
import { ApiService } from 'src/app/shared/services/api.service';
import { AuthService } from 'src/app/shared/services/auth.service';

@Component({
  selector: 'app-wish',
  templateUrl: './wish.component.html',
  styleUrls: ['./wish.component.scss']
})
export class WishComponent implements OnInit {
  ADD_IMAGE = ADD_IMAGE;
  EDIT = EDIT;
  EXTERNAL_LINK = EXTERNAL_LINK;
  CHECK = CHECK;
  CLOSE = CLOSE;
  AVATAR = AVATAR;
  DELETE = DELETE;

  wish: IWish = {
    ID: -1,
    Wish: "",
    Description: "",
    Price: -1,
    Link: "",
    Owner: -1,
    Login: ""
  };
  ownerInfo: IUser | null = null

  owner: boolean = false;

  private _error: boolean | undefined = undefined;
  set error(state: boolean | undefined) {
    if(state) { setTimeout(()=> this.error = false, 3000) }
    this._error = state
  }
  get error(): boolean | undefined{
    return this._error
  }

  constructor(
    private readonly activatedRoute: ActivatedRoute,
    private readonly apiService: ApiService,
    private readonly authService: AuthService,
    private readonly router: Router,
  ) { 
    this.activatedRoute.params.pipe(
      pluck('id'),
      switchMap(id => {
        if(id !== "create") {
          return this.apiService.getWish(+id)
        } else {
          return of(null)
        }
      })
    ).subscribe(wish => { 
      if(wish) {
        this.wish = {
          ...this.wish,
          ...wish
        }
        if(this.wish.Owner === this.authService.userAuthorizationData?.id) {
          this.owner = true
        }
      } else {
        this.owner = true
        this.wish = {
          ...this.wish,
          Owner: this.authService.userAuthorizationData?.id ?? -1,
          Login: this.authService.userAuthorizationData?.login ?? "",
          //TODO add request to user data
        }
        
      }
      if(this.wish.Owner !== -1 && this.wish.Login !== "") {
        this.apiService.getUserInfo(this.wish.Login)
        .subscribe((ownerInfo) => {
          this.ownerInfo = ownerInfo
        })
      }
    })
  }

  ngOnInit() {
  }

  openOwner() {
    if(this.ownerInfo) {
      this.router.navigate(["profile", this.ownerInfo.Login])
    }
  }

  deleteWish() {
    if(this.authService.userAuthorizationData) {
      this.apiService.deleteWish(
        this.authService.userAuthorizationData,
        this.wish.ID
      ).subscribe(()=>this.close())
    }
  }

  submit() {
    if(this.wish.Wish.length < 3) {
      this.error = true;
      return
    }

    if(this.authService.userAuthorizationData) {
      if(this.wish.ID === -1) {
        this.apiService.createWish(
          this.authService.userAuthorizationData,
          this.wish
        ).subscribe(() => {this.close()})
      } else {
        this.apiService.updateWish(
          this.authService.userAuthorizationData,
          this.wish
        ).subscribe(() => {this.close()})
      }
    }
    
  }

  close() {
    this.router.navigate([""])
  }

  openLink(link: string | undefined) {
    if(link) window.open(link);
  }

  onWishNameChange(event: Event) { 
    this.wish.Wish = (event.target as HTMLInputElement).value
  }
  onWishDescriptionChange(event: Event) {
    this.wish.Description = (event.target as HTMLInputElement).value
  }
  onWishPriceChange(event: Event) {
    this.wish.Price = +(event.target as HTMLInputElement).value
  }
  onWishLinkChange(event: Event) {
    this.wish.Link = (event.target as HTMLInputElement).value
  }
  onWishImageChange(event: any) {
    let files: FileList = event.target.files
    if(files.length === 1) {
      let file = files[0];
      if(file.size > MAX_IMAGE_SIZE*1024) {
        this.error = true
        return
      } else {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            this.wish.Image = reader.result?.toString()
        };
        reader.onerror = () => {
          this.error = true;
          return
        }
      }
    } else this.error = true
  }
}