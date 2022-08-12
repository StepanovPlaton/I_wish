import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { TranslateModule } from '@ngx-translate/core';
import { PasswordInputWithEyeModule } from '../../base/password-input-with-eye/password-input-with-eye.module';
import { MainRoutingModule } from './main-routing.component';
import { MainComponent } from './main.component';
import { WishListModule } from 'src/app/base/wish-list/wish-list.module';

@NgModule({
  imports: [
    CommonModule,
    MainRoutingModule,
    IonicModule,
    TranslateModule,
    PasswordInputWithEyeModule,
    WishListModule,
  ],
  declarations: [MainComponent],
  exports: [],
})
export class MainModule {}
