## Improving current RPM spec files
Most RPM spec files can be improved. I'm talking about the small things like adding licenses with the `%license` or `%doc` files in `%files` section or splitting up packages like `libunity` and `libunity-devel`. This is a bit of a concern but should get better over time.

## Adding RPM spec files
Before adding RPM spec files in a pull request, they **must** be related to Unity-shell or any packages that were added that the package needs since RPM repositories cannot provide them because they do not have libunity, xpathselect, etc.