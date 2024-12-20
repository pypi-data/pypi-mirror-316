[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.28.3...0.29.0)

### New

- Add support for specifying current version in `do_show`. [878197f](https://github.com/callowayproject/bump-my-version/commit/878197f186defabf036ddeb940eb91dfed172d0b)
    
  This update introduces a `--current-version` option to the `show` command and passes it into the `do_show` function. If provided, the `current_version` is added to the configuration, allowing more control over version display or manipulation.
### Updates

- Update README to clarify pre_n handling with distance_to_latest_tag. [c027879](https://github.com/callowayproject/bump-my-version/commit/c0278791fad3de1c3d66ab06b49118b2b8314933)
    
  Revised the `parse` expression to exclude `pre_n` and updated `serialize` examples to use `distance_to_latest_tag` instead. Fixes #272
