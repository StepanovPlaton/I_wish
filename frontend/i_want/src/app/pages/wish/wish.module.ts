import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { TranslateModule } from '@ngx-translate/core';
import { PasswordInputWithEyeModule } from '../../base/password-input-with-eye/password-input-with-eye.module';
import { WishComponent } from './wish.component';
import { WishRoutingModule } from './wish-routing.component';

@NgModule({
  imports: [
    CommonModule,
    WishRoutingModule,
    IonicModule,
    TranslateModule,
    PasswordInputWithEyeModule,
  ],
  declarations: [
    WishComponent
  ],
  exports: []
})
export class WishModule { }
