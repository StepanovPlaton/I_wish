import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PasswordInputWithEyeComponent } from './password-input-with-eye.component';
import { IonicModule } from '@ionic/angular';

@NgModule({
  imports: [
    CommonModule,
    IonicModule,
  ],
  declarations: [PasswordInputWithEyeComponent],
  exports: [PasswordInputWithEyeComponent]
})
export class PasswordInputWithEyeModule { }
