import { Component, ContentChild, OnInit } from '@angular/core';
import { IonInput } from '@ionic/angular';

@Component({
  selector: 'app-password-input-with-eye',
  templateUrl: './password-input-with-eye.component.html',
  styleUrls: ['./password-input-with-eye.component.scss']
})
export class PasswordInputWithEyeComponent implements OnInit {
  @ContentChild(IonInput) input: IonInput | undefined;

  showPassword = false;

  constructor() { }

  ngOnInit() {
  }
  toggleShow() {
    this.showPassword = !this.showPassword;
    if(this.input) {
      this.input.type = this.showPassword ? 'text' : 'password';
    }
  }

}
