import { Component } from '@angular/core';
import { MenuService } from './_services/menu.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'thesis_project';

  constructor(menuService: MenuService) {
    menuService.initMenu();
  }
}
