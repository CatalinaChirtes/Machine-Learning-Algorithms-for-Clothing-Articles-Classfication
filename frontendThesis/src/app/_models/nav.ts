export interface NavItem {
    displayName: string;
    disabled?: boolean;
    expanded?: boolean;
    iconName: string;
    route?: string;
    children?: NavItem[];
    claim?: string;
  }
  