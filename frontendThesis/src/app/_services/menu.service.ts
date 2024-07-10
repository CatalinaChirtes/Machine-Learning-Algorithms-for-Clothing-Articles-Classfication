import { Injectable } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { NavItem } from '../_models/nav';
import { TranslateService } from '@ngx-translate/core';

@Injectable({
  providedIn: 'root'
})
export class MenuService {
  public displayComponentHeader = false;

  public main: NavItem[] = [];

  public components: NavItem[] = [];

  public currentUrl = new BehaviorSubject<string>('');

  constructor(private router: Router, private translate: TranslateService) {
    setTimeout(() => {
      this.initMenu();
    }, 1000);
    this.router.events.subscribe((event) => {
      this.findMenuItem(event);
      setTimeout(() => {
        this.findMenuItem(event);
      }, 1000);
      if (event instanceof NavigationEnd) {
        this.currentUrl.next(event.urlAfterRedirects);
      }
    });
  }

  public initMenu() {
    this.main = [];
    this.components = [];

    this.translate.get('menu.componentMenu.cnn-model').subscribe((name) => {
      this.components.push({
        displayName: name,
        iconName: 'layers',
        route: '/cnn-model'
      });
    });
    this.translate.get('menu.componentMenu.mobile-net-v2-model').subscribe((name) => {
      this.components.push({
        displayName: name,
        iconName: 'install_mobile',
        route: '/mobile-net-v2-model'
      });
    });
    this.translate.get('menu.componentMenu.inception-res-net-v2-model').subscribe((name) => {
      this.components.push({
        displayName: name,
        iconName: 'install_mobile',
        route: '/inception-res-net-v2-model'
      });
    });
  }

  private findMenuItem(event: any) {
    let menuItem = [];
    const temp1 = this.main.filter((i) => i.route === event.url);
    const temp2 = this.components.filter((i) => i.route === event.url);
    if (temp1.length > 0) {
      menuItem = temp1;
    } else if (temp2.length > 0) {
      menuItem = temp2;
    } else {
      return;
    }
    if (menuItem[0].disabled) {
      this.router.navigate(['/']);
    }
  }
}
