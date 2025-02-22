import { Button } from "@/components/ui/button";
import {
    RiFacebookFill,
    RiGithubFill,
    RiGoogleFill,
    RiTwitterXFill,
} from "@remixicon/react";

const SocialAuthentication = () => {
    return (
        <div className="flex flex-col gap-2">
            <Button variant="outline" disabled>
                <RiGoogleFill
                    className="me-1 text-[#DB4437] dark:text-white/60"
                    size={16}
                    aria-hidden="true"
                />
                Login with Google
            </Button>
            <Button variant="outline" disabled>
                <RiTwitterXFill
                    className="me-1 text-[#14171a] dark:text-white/60"
                    size={16}
                    aria-hidden="true"
                />
                Login with X
            </Button>
            <Button variant="outline" disabled>
                <RiFacebookFill
                    className="me-1 text-[#1877f2] dark:text-white/60"
                    size={16}
                    aria-hidden="true"
                />
                Login with Facebook
            </Button>
            <Button variant="outline" disabled>
                <RiGithubFill
                    className="me-1 text-[#333333] dark:text-white/60"
                    size={16}
                    aria-hidden="true"
                />
                Login with GitHub
            </Button>
        </div>
    );
};

export default SocialAuthentication;
