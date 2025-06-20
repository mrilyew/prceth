from db.LinkManager import link_manager

class ExportManager:
    async def exportContentUnit(cu, args):
        dir_path = args.get('dir_path')
        file_prefix = args.get('file_prefix', '')
        recursion_level = args.get('recursion_level', 0)
        recursion_level_limit = args.get('recursion_level_limit', 5)
        save_json = args.get('save_json', False)
        if recursion_level > recursion_level_limit:
            return None

        if args.get('export_linked', True) == True:
            links = link_manager.linksList(cu)
            for link in links:
                link.export(dir_path=dir_path,save_json=save_json,recursion_level=recursion_level+1,recursion_level_limit=recursion_level_limit)

        if save_json == True:
            cu.save_info_to_json(dir_path)

export_manager = ExportManager()
