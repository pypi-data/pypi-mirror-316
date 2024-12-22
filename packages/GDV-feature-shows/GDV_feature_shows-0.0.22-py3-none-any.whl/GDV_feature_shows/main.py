# coding: utf-8

from GDV_feature_shows.interface import App
from GDV_feature_shows.resource_manager import ResourceManager
from GDV_feature_shows.feature_extraction import FeatureExtractor
from GDV_feature_shows.parsing import get_args


def main():
    args = get_args()
    FeatureExtractor()
    ResourceManager()
    app = App(args.gdv_path, args.settings_path)
    app.mainloop()


if __name__ == "__main__":
    main()
